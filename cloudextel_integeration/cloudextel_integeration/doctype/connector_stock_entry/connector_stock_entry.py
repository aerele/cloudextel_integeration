# Copyright (c) 2022, CloudExtel and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

@frappe.whitelist()
def create_stock_entry():
	entry = frappe.db.sql("""select name  from `tabConnector Stock Entry` where  is_synced =0 and retry_limit>0 order by creation desc limit 20""",as_dict=1)
	for cse in entry:
		try:
			new_stock_entry(cse.name)
		except:
			pass

@frappe.whitelist()
def new_stock_entry(name):
	cse = frappe.get_doc("Connector Stock Entry",name)
	reference = frappe.db.get_value("Stock Entry", {"reference_no":cse.reference_no, "docstatus":1})
	if reference:
		frappe.throw("Reference No already exists")
	frappe.db.sql("""update `tabConnector Stock Entry` set retry_limit=retry_limit-1 where name='%s' """,(name))
	frappe.db.commit()
	submit_se = frappe.db.get_value("Api Settings", "Api Settings", 'submit_delivery_note')
	doc = frappe.new_doc("Stock Entry")
	doc.company = cse.company
	doc.stock_entry_type = "Material Transfer"
	doc.purpose = "Material Transfer"
	doc.set_posting_time = 1
	doc.posting_time = cse.posting_time
	doc.posting_date = cse.posting_date
	doc.reference_no = cse.reference_no
	doc.from_warehouse = frappe.db.get_value("Warehouse", {"odwen_warehouse_id": cse.from_warehouse}, 'name') or None
	if not doc.from_warehouse:
		frappe.throw("Couldn't find warehouse with id "+cse.from_warehouse)
	doc.to_warehouse = frappe.db.get_value("Warehouse", {"odwen_warehouse_id": cse.to_warehouse}, 'name') or None
	if not doc.to_warehouse:
		frappe.throw("Couldn't find warehouse with id "+cse.to_warehouse)
	doc.delivery_to = doc.to_warehouse
	doc.items = get_items(cse, doc.from_warehouse, doc.to_warehouse)
	try:
		doc.save(ignore_permissions=True)
		frappe.db.sql("""update `tabConnector Stock Entry` set is_synced= 1, status='Synced' where name= %s""",(cse.name))
		frappe.db.commit()
		if submit_se == 'Yes':
			doc.submit()
		frappe.db.commit()
		frappe.msgprint("Stock Entry Created: {0}".format(frappe.utils.get_link_to_form("Stock Entry", doc.name, doc.name)))
		return True
	except Exception as e:
		frappe.errprint(e)
		return False

def get_items(cse, from_warehouse, to_warehouse):
	items = []
	for i in cse.items:
		items.append(frappe.get_doc({
			'doctype': "Stock Entry Detail",
			'parentfield':"items",
			'parenttype': "Stock Entry",
			's_warehouse': from_warehouse,
			't_warehouse':to_warehouse,
			'item_code': i.item_code,
			'qty': i.qty,
			'uom': i.uom,
			'conversion_factor': 1,
			'basic_amount': 0
		}))
	return items
class ConnectorStockEntry(Document):
	pass
