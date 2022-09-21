import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def after_install():
	make_custom_fields()

def make_custom_fields():
	custom_fields = {
		'Stock Entry': [],
		'Sales Order': [],
		'Delivery Note': [],
		'Purchase Order': [],
		'Purchase Receipt': [],
		'Warehouse': []
	}
	print("Stock Entry")
	if not frappe.get_meta("Stock Entry").get_field("reference_no"):
		custom_fields["Stock Entry"].append(dict(fieldname='reference_no', label='Reference No',
						fieldtype='Data', insert_after='apply_putaway_rule'))

	print("Sales Order")
	if not frappe.get_meta("Sales Order").get_field("odwen_order_no"):
		custom_fields["Sales Order"].append(dict(fieldname='odwen_order_no', label='Odwen Order No',
						fieldtype='Data', insert_after='skip_delivery_note'))

	print("Delivery Note")
	if not frappe.get_meta("Delivery Note").get_field("reference_no"):
		custom_fields["Delivery Note"].append(dict(fieldname='reference_no', label='Reference No',
						fieldtype='Data', insert_after='customer_name'))

	print("Purchase Order")
	if not frappe.get_meta("Purchase Order").get_field("odwen_order_no"):
		custom_fields["Purchase Order"].append(dict(fieldname='odwen_order_no', label='Odwen Order No',
						fieldtype='Data', insert_after='tax_withholding_category'))

	print("Purchase Receipt")
	if not frappe.get_meta("Purchase Receipt").get_field("reference_no"):
		custom_fields["Purchase Receipt"].append(dict(fieldname='reference_no', label='Reference No',
						fieldtype='Data', insert_after='supplier_delivery_note'))

	print("Warehouse")
	if not frappe.get_meta("Warehouse").get_field("odwen_warehouse_id"):
		custom_fields["Warehouse"].append(dict(fieldname='odwen_warehouse_id', label='Odwen Warehouse ID',
						fieldtype='Data', insert_after='is_group'))

	create_custom_fields(custom_fields)