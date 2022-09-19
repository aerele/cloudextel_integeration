import frappe


def get_api_key():
	api_key = frappe.db.get_value("Api Settings", "Api Settings", "api_key")
	if not api_key:
		frappe.throw("Add api key in {0}".format(frappe.utils.get_link_to_form(doctype="Api Settings", name="", label="Api Settings")))
	return api_key

def get_url():
	url = frappe.db.get_value("Api Settings", "Api Settings", "url")
	if not url:
		frappe.throw("Add api url in {0}".format(frappe.utils.get_link_to_form(doctype="Api Settings", name="", label="Api Settings")))
	return url

def supplier(self, method):
	key = get_api_key()
	url = get_url()
	supplier_path = frappe.db.get_value("Api Settings", "Api Settings", "supplier")
	if not supplier_path:
		frappe.throw("Add api supplier endpoint in {0}".format(frappe.utils.get_link_to_form(doctype="Api Settings", name="", label="Api Settings")))
	url += supplier_path
	payload = frappe._dict({
			"key":key or '',
			"vendor_code": self.name,
			"vendor_name": self.supplier_name,
			"email":"",
			"phone_number":"",
			"gst_number":"",
			"address1":"",
			"address2":"",
			"state":"",
			"city":"",
			"pincode":""
		}
	)
	header = {
		"Content-Type":"application/json"
	}
	if self.supplier_primary_contact:
		contact = frappe.get_doc("Contact", self.supplier_primary_contact)
		for i in contact.email_ids:
			if  i.is_primary:
				payload.email = i.email_id
				break
		for i in contact.phone_nos:
			if i.is_primary_mobile_no:
				payload.phone_number = i.phone
				break
	if self.supplier_primary_address:
		address = frappe.get_doc("Address", self.supplier_primary_address)
		payload.gst_number = address.gstin
		payload.address1 = address.address_line1
		payload.address2 = address.address_line2
		payload.state = address.state
		payload.city = address.city
		payload.pincode = address.pincode

	make_api_call(url, payload, header)


def customer(self, method):
	key = get_api_key()
	url = get_url()
	customer_path = frappe.db.get_value("Api Settings", "Api Settings", "customer")
	if not customer_path:
		frappe.throw("Add api customer endpoint in {0}".format(frappe.utils.get_link_to_form(doctype="Api Settings", name="", label="Api Settings")))
	url += customer_path
	payload = frappe._dict(
		{
			"key": key,
			"customer_code": self.name,
			"customer_name":self.customer_name,
			"email": "",
			"phone_number": "",
			"gst_number": "",
			"shipping_address1": "",
			"shipping_address2": "",
			"shipping_state": "",
			"shipping_city": "",
			"shipping_postalcode": "",
			"billing_address1":"",
			"billing_address2":"",
			"billing_state":"",
			"billing_city":"",
			"billing_postalcode":""
		}
	)
	header = {
		"Content-Type":"application/json"
	}
	if self.customer_primary_contact:
		contact = frappe.get_doc("Contact", self.supplier_primary_contact)
		for i in contact.email_ids:
			if  i.is_primary:
				payload.email = i.email_id
				break
		for i in contact.phone_nos:
			if i.is_primary_mobile_no:
				payload.phone_number = i.phone
				break
	billing_address = frappe.db.sql(""" select distinct ad.name from `tabAddress` as ad join `tabDynamic Link` as dl on dl.parent=ad.name where dl.link_doctype='Customer' and dl.link_name='{0}' and ad.is_primary_address=1 order by ad.modified desc""".format(self.name))
	shipping_address = frappe.db.sql(""" select distinct ad.name from `tabAddress` as ad join `tabDynamic Link` as dl on dl.parent=ad.name where dl.link_doctype='Customer' and dl.link_name='{0}' and ad.is_shipping_address=1 order by ad.modified desc""".format(self.name))

	if shipping_address and len(shipping_address):
		ship_address = frappe.get_doc("Address", billing_address[0][0])
		payload.gst_number = ship_address.gstin
		payload.shipping_address1 = ship_address.address_line1
		payload.shipping_address2 = ship_address.address_line2
		payload.shipping_state = ship_address.state
		payload.shipping_city = ship_address.city
		payload.shipping_postalcode = ship_address.pincode

	if billing_address and len(billing_address):
		bill_address = frappe.get_doc("Address", billing_address[0][0])
		payload.gst_number = bill_address.gstin or ship_address.gstin
		payload.billing_address1 = bill_address.address_line1
		payload.billing_address2 = bill_address.address_line2
		payload.billing_state = bill_address.state
		payload.billing_city = bill_address.city
		payload.billing_postalcode = bill_address.pincode

	make_api_call(url, payload, header)

def address_and_contact(self, method):
	for i in self.links:
		if i.link_doctype == "Supplier":
			supplier_doc = frappe.get_doc("Supplier", i.link_name)
			supplier(supplier_doc, method)
		elif i.link_doctype == "Customer":
			customer_doc = frappe.get_doc("Customer", i.link_name)
			customer(customer_doc, method)

def create_sales_order(self, method):
	key = get_api_key()
	url = get_url()
	sales_order = frappe.db.get_value("Api Settings", "Api Settings", "sales_order")
	if not sales_order:
		frappe.throw("Add api supplier endpoint in {0}".format(frappe.utils.get_link_to_form(doctype="Api Settings", name="", label="Api Settings")))
	url += sales_order
	payload = frappe._dict({
		  "key": key,
		  "customer_code":self.customer ,
		  "warehouse_booking_id": 225,
		  "erpnext_ref_id": self.name,
		  "comment":"",
		  "invoice_no":self.name,
		  "invoice_date": self.transaction_date,
		  "expected_delivery_date": self.delivery_date,
		  "line_items": []
		}
	)
	for i in self.items:
		payload.line_items.append({
			"item_code": i.item_code,
			"quantity": i.qty
		})

	header = {
		"Content-Type":"application/json"
	}
	make_api_call(url, payload, header, self.doctype)

def create_purchase_order(self, method):
	key = get_api_key()
	url = get_url()
	purchase_order = frappe.db.get_value("Api Settings", "Api Settings", "purchase_order")
	if not purchase_order:
		frappe.throw("Add api supplier endpoint in {0}".format(frappe.utils.get_link_to_form(doctype="Api Settings", name="", label="Api Settings")))
	url += purchase_order
	payload = frappe._dict({
	  "key": key,
	  "vendor_code": self.supplier,
	  "warehouse_booking_id": 225,
	  "erpnext_ref_id": self.name,
	  "comment":"",
	  "invoice_no": self.name,
	  "invoice_date": self.transaction_date,
	  "expected_delivery_date": self.schedule_date,
	  "line_items": []
		}
	)
	for i in self.items:
		payload.line_items.append({
			"item_code": i.item_code,
			"quantity": i.qty
		})

	header = {
		"Content-Type":"application/json"
	}
	make_api_call(url, payload, header, self.doctype)

def cancel_sales_order(self, method):
	key = get_api_key()
	url = get_url()
	cancel_so = frappe.db.get_value("Api Settings", "Api Settings", "cancel_sales_order")
	if not cancel_so:
		frappe.throw("Add api Cancel Sales Order endpoint in {0}".format(frappe.utils.get_link_to_form(doctype="Api Settings", name="", label="Api Settings")))
	url += cancel_so
	payload = frappe._dict({
		  "key":key,
		  "odwen_so_number":self.odwen_order_no,
		  "cancel_reason": 1,
		  "cancel_comment": "",
		}
	)

	header = {
		"Content-Type":"application/json"
	}
	make_api_call(url, payload, header)


def item(self, method):
	key = get_api_key()
	url = get_url()
	item_path = frappe.db.get_value("Api Settings", "Api Settings", "supplier")
	if not item_path:
		frappe.throw("Add api item endpoint in {0}".format(frappe.utils.get_link_to_form(doctype="Api Settings", name="", label="Api Settings")))
	url += item_path
	payload = frappe._dict({
			"key": key,
			"item_code": self.name,
			"item_name": self.item_name,
			"item_category": self.item_group,
			"picking_rule_apply":"yes" if self.has_batch_no else 'no',
			"gst_number":"",
			"unit_of_measurement": self.stock_uom,
			"shelf_life":"",
			"brand_name":"",
			"model_number":"",
			"item_color":"",
			"reorder_level":0,
			"packing_after_grn":"yes",
			"base_price":"",
			"selling_price":"",
			"storage_type":"",
		}
	)
	header = {
		"Content-Type":"application/json"
	}
	price = frappe.db.get_value("Item Price", {"item_code": self.name, "selling":1}, "price_list_rate") or 0
	payload.base_price = price
	payload.selling_price = price
	make_api_call(url, payload, header)



def make_api_call(url, payloads, header, doctype=None):
	import requests
	import json

	payload = json.dumps(payloads)
	headers = header
	new_doc = frappe.new_doc("Webhook Request Log")
	new_doc.user = frappe.session.user
	new_doc.url = url
	new_doc.headers = json.dumps(headers)
	new_doc.data = payload

	try:
		response = requests.request("POST", url, headers=headers, data=payload)
		new_doc.response = response.text
		res = json.loads(response.text.strip())
		if response.status_code == 200 and res["status"] == 1 and doctype:
			order_no = res["odwen_so_number"] if doctype == "Sales Order" else res["odwen_po_number"]
			frappe.db.set_value(doctype, payloads.erpnext_ref_id, "odwen_order_no", order_no)
	except Exception as e:
		frappe.msgprint(res['message'])
		new_doc.response = e
	new_doc.insert(ignore_permissions=True)


