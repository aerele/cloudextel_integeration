# Copyright (c) 2022, CloudExtel and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from erpnext.buying.doctype.purchase_order.purchase_order import make_purchase_receipt
class ConnectorPurchaseReceipt(Document):
	pass



@frappe.whitelist()
def create_purchase_receipt():
	orders = frappe.db.sql("""select name  from `tabConnector Purchase Receipt` where  is_synced =0 and retry_limit>0 order by creation desc limit 20""",as_dict=1)
	for purchase_receipt_id in orders:
		try:
			new_purchasereceipt(purchase_receipt_id.name)
		except:
			pass


@frappe.whitelist()
def new_purchasereceipt(purchase_receipt_id):
	pr_doc = frappe.get_doc("Connector Purchase Receipt",purchase_receipt_id)
	reference = frappe.db.get_value("Purchase Receipt", {"reference_no":pr_doc.reference_no, "docstatus":1})
	if reference:
		frappe.throw("Reference No already exists")
	frappe.db.sql("""update `tabConnector Purchase Receipt` set retry_limit=retry_limit-1 where name= %s """,(purchase_receipt_id))
	submit_pr = frappe.db.get_value("Api Settings", "Api Settings", 'submit_delivery_note')
	purchase_receipt=make_purchase_receipt(pr_doc.purchase_order_no)
	purchase_receipt.reference_no = pr_doc.reference_no
	purchase_receipt.set_posting_time = 1
	purchase_receipt.posting_time = pr_doc.posting_time
	purchase_receipt.posting_date = pr_doc.posting_date
	c_item = {}
	p_item=[]
	for i in pr_doc.items:
		c_item[i.item_code] = i
	for item in (purchase_receipt.items):
		if	item.item_code in c_item:
			c_it = c_item[item.item_code]
			item.received_qty= c_it.received_qty
			item.qty=c_it.qty
			item.rejected_qty=c_it.rejected_qty
			p_item.append(item)
	purchase_receipt.items=p_item
	purchase_receipt.rejected_warehouse = purchase_receipt.set_warehouse
	try:
		purchase_receipt.save(ignore_permissions=True)
		frappe.db.sql("""update `tabConnector Purchase Receipt` set is_synced= 1, status='Synced' where name= %s""",(pr_doc.name))
		frappe.db.commit()
		if submit_pr == 'Yes':
			purchase_receipt.submit()
		frappe.db.commit()
		return True
	except Exception as e:
		frappe.errprint(e)
		return False