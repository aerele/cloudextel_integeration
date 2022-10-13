# Copyright (c) 2022, CloudExtel and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from erpnext.selling.doctype.sales_order.sales_order import make_delivery_note

class ConnectorDeliveryNote(Document):
	pass


@frappe.whitelist()
def create_delivery_note():
	orders = frappe.db.sql("""select name  from `tabConnector Delivery Note` where  is_synced =0 and retry_limit>0 order by creation desc limit 20""",as_dict=1)
	for delivery_note_id in orders:
		try:
			new_delivery_note(delivery_note_id.name)
		except:
			pass

@frappe.whitelist()
def create_dn(name):
	dn_doc = frappe.get_doc("Connector Delivery Note",name)
	if frappe.db.get_value("Sales Order", dn_doc.sales_order):
		new_delivery_note(name)
	elif frappe.db.get_value("Material Request", dn_doc.sales_order):
		new_material_issue(name)

def new_material_issue(name):
	dn_doc = frappe.get_doc("Connector Delivery Note",name)
	mr = frappe.get_doc("Material Request", dn_doc.sales_order)
	reference = frappe.db.get_value("Stock Entry", {"reference_no":dn_doc.reference_no, "docstatus":1})
	if reference:
		frappe.throw("Reference No already exists")
	frappe.db.sql("""update `tabConnector Delivery Note` set retry_limit=retry_limit-1 where name='{0}' """.format(name))
	frappe.db.commit()
	submit_se = frappe.db.get_value("Api Settings", "Api Settings", 'submit_delivery_note')
	doc = frappe.new_doc("Stock Entry")
	doc.company = mr.company
	doc.stock_entry_type = "Material Issue"
	doc.set_posting_time = 1
	doc.posting_time = dn_doc.posting_time
	doc.posting_date = dn_doc.posting_date
	doc.reference_no = dn_doc.reference_no
	doc.material_request = dn_doc.sales_order
	doc.from_warehouse = frappe.db.get_value("Warehouse", {"odwen_warehouse_id": dn_doc.set_warehouse}, 'name') or None
	if not doc.from_warehouse:
		frappe.throw("Couldn't find warehouse with id "+dn_doc.set_warehouse)
	is_return = has_return(dn_doc.items)
	if is_return:
		doc.stock_entry_type = "Material Receipt"
		doc.items = get_return_items(dn_doc, doc.from_warehouse)
		doc.to_warehouse = doc.from_warehouse
	else:
		doc.items = get_sales_items(dn_doc, doc.from_warehouse)
		doc.stock_entry_type = "Material Issue"
	try:
		doc.save(ignore_permissions=True)
		frappe.db.sql("""update `tabConnector Delivery Note` set is_synced= 1, status='Synced' where name='{0}'""".format(dn_doc.name))
		frappe.db.commit()
		if submit_se == 'Yes':
			doc.submit()
		frappe.db.commit()
		frappe.msgprint("Stock Entry Created: {0}".format(frappe.utils.get_link_to_form("Stock Entry", doc.name, doc.name)))
		return True
	except Exception as e:
		frappe.errprint(e)
		return False

def has_return(items):
	for i in items:
		if i.qty < 0:
			return True
	return False

def get_sales_items(cse, from_warehouse):
	items = []
	for i in cse.items:
		items.append(frappe.get_doc({
			'doctype': "Stock Entry Detail",
			'parentfield':"items",
			'parenttype': "Stock Entry",
			's_warehouse': from_warehouse,
			'item_code': i.item_code,
			'qty': abs(i.qty),
			'uom': i.uom or frappe.db.get_value("Item", i.item_code, "stock_uom"),
			'conversion_factor': 1,
			'basic_amount': 0
		}))
	return items

def get_return_items(cse, to_warehouse):
	items = []
	for i in cse.items:
		items.append(frappe.get_doc({
			'doctype': "Stock Entry Detail",
			'parentfield':"items",
			'parenttype': "Stock Entry",
			't_warehouse': to_warehouse,
			'item_code': i.item_code,
			'qty': abs(i.qty),
			'uom': i.uom or frappe.db.get_value("Item", i.item_code, "stock_uom"),
			'conversion_factor': 1,
			'basic_amount': 0
		}))
	return items


def new_delivery_note(delivery_note_id):
	dn_doc = frappe.get_doc("Connector Delivery Note",delivery_note_id)
	reference = frappe.db.get_value("Delivery Note", {"reference_no":dn_doc.reference_no, "docstatus":1})
	if reference:
		frappe.throw("Reference No already exists")
	frappe.db.sql("""update `tabConnector Delivery Note` set retry_limit=retry_limit-1 where name='{0}' """.format(delivery_note_id))
	frappe.db.commit()
	submit_dn = frappe.db.get_value("Api Settings", "Api Settings", 'submit_delivery_note')
	delivery_note=make_delivery_note(dn_doc.sales_order)
	delivery_note.reference_no = dn_doc.reference_no
	delivery_note.set_posting_time = 1
	delivery_note.posting_time = dn_doc.posting_time
	delivery_note.posting_date = dn_doc.posting_date
	c_item = {}
	p_item=[]
	for i in dn_doc.items:
		c_item[i.item_code] = i
	for item in (delivery_note.items):
		if item.item_code in c_item:
			so_item_doc = frappe.db.get_value("Sales Order Items", {"item_code": item.item_code, "parent":dn_doc.sales_order}, "cost_center")
			c_it = c_item[item.item_code]
			item.qty=c_it.qty
			item.cost_center = so_item_doc
			p_item.append(item)
	delivery_note.items=p_item
	try:
		delivery_note.save(ignore_permissions=True)
		frappe.db.sql("""update `tabConnector Delivery Note` set is_synced= 1, status='Synced' where name='{0}'""".format(dn_doc.name))
		frappe.db.commit()
		if submit_dn == 'Yes':
			delivery_note.submit()
		frappe.db.commit()
		frappe.msgprint("Delivery Note Created: {0}".format(frappe.utils.get_link_to_form("Delivery Note", delivery_note.name, delivery_note.name)))
		return True
	except Exception as e:
		frappe.errprint(e)
		return False