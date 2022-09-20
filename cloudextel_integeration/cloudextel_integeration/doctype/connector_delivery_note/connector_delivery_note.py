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
	delivery_note=make_delivery_note(dn_doc.purchase_order_no)
	delivery_note.reference_no = dn_doc.reference_no
	c_item = {}
	p_item=[]
	for i in dn_doc.items:
		c_item[i.item_code] = i
	for item in (delivery_note.items):
		if	item.item_code in c_item:
			c_it = c_item[item.item_code]
			item.received_stock_qty= c_it.received_stock_qty
			item.stock_qty=c_it.stock_qty
			item.returned_qty=c_it.returned_qty
			p_item.append(item)
	delivery_note.items=p_item
	try:
		delivery_note.save(ignore_permissions=True)
		frappe.db.sql("""update `tabConnector Delivery Note` set is_synced= 1 where name= %s""",(dn_doc.name))
		frappe.db.commit()
	except Exception as e:
		frappe.errprint(e)