import frappe



@frappe.whitelist()
def create_purchase_receipt(args):
	try:
	# doc_name = []
	# for i in args:
		args['doctype'] = 'Connector Purchase Receipt'
		args['status'] = 'Pending'
		args['sync'] = 0
		doc = frappe.get_doc(args)
		doc.save()
	# doc_name.append(doc.name)
		return doc.name
	except Exception as e:
		raise Exception("Please try again later")


@frappe.whitelist()
def create_delivery_note(args):
	try:
		args['doctype'] = 'Connector Delivery Note'
		args['status'] = 'Pending'
		args['sync'] = 0
		doc = frappe.get_doc(args)
		doc.save()
		return doc.name
	except Exception as e:
		raise Exception("Please try again later")


@frappe.whitelist()
def create_stock_entry(args):
	try:
		args['doctype'] = 'Connector Stock Entry'
		args['status'] = 'Pending'
		args['sync'] = 0
		args['stock_entry_type'] = "Material Transfer"
		doc = frappe.get_doc(args)
		doc.save()
		return doc.name
	except Exception as e:
		raise Exception("Please try again later")


def get_status(doctype, name):
	return frappe.db.get_value(doctype, {"reference_no": name}, "workflow_state") or ''