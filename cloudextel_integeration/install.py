import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def after_install():
	make_custom_fields()

def make_custom_fields():
	custom_fields = {
		'Stock Entry': [],
		'Sales Order': [],
		'Material Request': [],
		'Delivery Note': [],
		'Purchase Order': [],
		'Purchase Receipt': [],
		'Warehouse': []
	}

	if not frappe.get_meta("Stock Entry").get_field("reference_no"):
		custom_fields["Stock Entry"].append(dict(fieldname='reference_no', label='Reference No',
						fieldtype='Data', insert_after='apply_putaway_rule'))

	if not frappe.get_meta("Sales Order").get_field("odwen_order_no"):
		custom_fields["Sales Order"].append(dict(fieldname='odwen_order_no', label='Odwen Order No',
						fieldtype='Data', insert_after='skip_delivery_note'))

	if not frappe.get_meta("Material Request").get_field("odwen_order_no"):
		custom_fields["Material Request"].append(dict(fieldname='odwen_order_no', label='Odwen Order No',
						fieldtype='Data', insert_after='status'))

	if not frappe.get_meta("Delivery Note").get_field("reference_no"):
		custom_fields["Delivery Note"].append(dict(fieldname='reference_no', label='Reference No',
						fieldtype='Data', insert_after='customer_name'))

	if not frappe.get_meta("Purchase Order").get_field("odwen_order_no"):
		custom_fields["Purchase Order"].append(dict(fieldname='odwen_order_no', label='Odwen Order No',
						fieldtype='Data', insert_after='tax_withholding_category'))

	if not frappe.get_meta("Purchase Order").get_field("is_stock_transfer"):
		custom_fields["Purchase Order"].append(dict(fieldname='is_stock_transfer', label='Is Stock Transfer',
						fieldtype='Check', insert_after='odwen_order_no'))

	if not frappe.get_meta("Purchase Receipt").get_field("reference_no"):
		custom_fields["Purchase Receipt"].append(dict(fieldname='reference_no', label='Reference No',
						fieldtype='Data', insert_after='supplier_delivery_note'))

	if not frappe.get_meta("Warehouse").get_field("odwen_warehouse_id"):
		custom_fields["Warehouse"].append(dict(fieldname='odwen_warehouse_id', label='Odwen Warehouse ID',
						fieldtype='Data', insert_after='is_group'))

	create_custom_fields(custom_fields)