import frappe


def get_api_key():
	api_key = frappe.db.get_value("Api Settings", "Api Settings", "api_key")
	if not api_key:
		frappe.throw("Add api key in {0}".format(frappe.utils.get_link_to_form(doctype="Api Settings", name="", label="Api Settings")))
	return api_key

def address(self, method):
	key = get_api_key()
	api_func = {
		'Supplier': "vendor_add_edit",
		'Customer': "customer_add_edit"
	}
	url = "https://staging.odwen.co.in/api/erpnext/"
	for i in self.links:
		if i.link_doctype not in api_func:
			continue
		url += api_func[i.link_doctype]

		import requests
		import json

		payload = json.dumps({
			"key": key,
			"vendor_code": i.link_name,
			"vendor_name": i.link_type,
			"email": "",
			"phone_number": "",
			"gst_number": "",
			"address1": "",
			"address2": "",
			"state": "",
			"city": "",
			"pincode": ""
		})
		headers = {
			'Content-Type': 'application/json',
			'Cookie': 'CAKEPHP=rcsi3588cnjc887bec9pu8ig8r'
		}

		response = requests.request("POST", url, headers=headers, data=payload)

		print(response.text)

