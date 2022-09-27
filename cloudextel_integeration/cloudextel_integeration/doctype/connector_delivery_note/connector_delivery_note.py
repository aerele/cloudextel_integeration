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
def new_delivery_note(delivery_note_id):
	dn_doc = frappe.get_doc("Connector Delivery Note",delivery_note_id)
	reference = frappe.db.get_value("Delivery Note", {"reference_no":dn_doc.reference_no, "docstatus":1})
	if reference:
		frappe.throw("Reference No already exists")
	frappe.db.sql("""update `tabConnector Delivery Note` set retry_limit=retry_limit-1 where name= %s """,(delivery_note_id))
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
			so_item_doc = frappe.get_doc("Sales Order Items", {"item_code": item.item_code, "parent":dn_doc.sales_order})
			c_it = c_item[item.item_code]
			item.qty=c_it.qty
			item.cost_center = so_item_doc.cost_center
			p_item.append(item)
	delivery_note.items=p_item
	try:
		frappe.errprint(delivery_note)
		delivery_note.save(ignore_permissions=True)
		frappe.db.sql("""update `tabConnector Delivery Note` set is_synced= 1 where name= %s""",(dn_doc.name))
		frappe.db.commit()
		if submit_dn == 'Yes':
			delivery_note.submit()
		frappe.db.commit()
		return True
	except Exception as e:
		frappe.errprint(e)
		return False