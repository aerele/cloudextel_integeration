# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe

@frappe.whitelist()
def get_workflow_doctype(*args):
	return [[i.document_type] for i in frappe.db.get_list("Workflow", filters={'is_active':1}, or_filters={'document_type':['like', f'%{args[1]}%']}, fields=['distinct document_type'])]

def execute(filters=None):
	columns, data = [], []
	columns = get_columns(filters)
	data = get_data(filters)

	return columns, data

def get_data(filters):
	status_map = get_status_role_map(filters)
	from_date, to_date = filters.date
	data = []
	data_state = []
	for i in status_map:
		data_state.append(i+'_within_tat')
		data.append(
			{
				"doctype": filters.doctype,
				"workflow_state": i,
				"cost_center": "",
				"telecom_circle": "",
				"category": "Within TAT",
				status_map[i]+"_no_of_docs": 0,
				status_map[i]+"_avg_days": 0
			}
		)
		data_state.append(i+'_outside_tat')
		data.append(
			{
				"doctype": filters.doctype,
				"workflow_state": i,
				"cost_center": "",
				"telecom_circle": "",
				"category": "Outside TAT",
				status_map[i]+"_no_of_docs": 0,
				status_map[i]+"_avg_days": 0
			}
		)
	raw = frappe.db.get_list(filters.doctype, {"creation":[">", from_date], "creation":["<", to_date    ]}, order_by='creation')
	for i in raw:
		doc = frappe.get_doc(filters.doctype, i.name)
		if doc.workflow_state not in status_map:
			continue
		if doc.workflow_state+'_within_tat' in data_state or doc.workflow_state+"_outside_tat":
			age = get_age(doc.modified.date())
			if age <= 3 and age > 0:
				idx = data_state.index(doc.workflow_state+"_within_tat")
				role = status_map[doc.workflow_state]
				data[idx][role+"_no_of_docs"] += 1
				data[idx][role+"_avg_days"] = ((data[idx][role+"_avg_days"] + age) // 2) if data[idx][role+"_avg_days"]!=0 else age
			elif age > 3:
				idx = data_state.index(doc.workflow_state+"_outside_tat")
				role = status_map[doc.workflow_state]
				data[idx][role+"_no_of_docs"] += 1
				data[idx][role+"_avg_days"] = ((data[idx][role+"_avg_days"] + age) // 2) if data[idx][role+"_avg_days"]!=0 else age
	return data



def get_age(modified):
	from datetime import date
	return frappe.utils.date_diff(date.today(), modified) + 1
def get_status_role_map(filters):
	workflow = get_workflow(filters)
	if not workflow:
		return
	role_map = {}
	doc = frappe.get_doc("Workflow", workflow)
	for i in doc.transitions:
		role_map[i.state] = i.allowed
	return role_map

def get_columns(filters):
	columns = []
	columns.append(
		{
			"fieldname": "doctype",
			"label": "Doctype",
			"fieldtype": "Data"
		}
	)
	columns.append(
		{
			"fieldname": "workflow_state",
			"label": "Workflow State",
			"fieldtype": "Link",
			"options": "Workflow State"
		}
	)
	if frappe.get_meta(filters.doctype).get_field("cost_center"):
		columns.append(
			{
				"fieldname": "cost_center",
				"label": "Cost Center",
				"fieldtype": "Link",
				"options": "Cost Center"
			}
		)
	if frappe.get_meta(filters.doctype).get_field("telecom_circle"):
		columns.append(
			{
				"fieldname": "telecom_circle",
				"label": "Telecom Circle",
				"fieldtype": "Link",
				"options": "Telecom Circle"
			}
		)
	columns.append(
		{
			"fieldname": "category",
			"label": "Category",
			"fieldtype": "Data"
		}
	)
	workflow = get_workflow(filters)
	if not workflow:
		return columns
	roles = get_workflow_roles(workflow)
	for i in roles:
		columns.append({
			"fieldname": i.allowed+"_no_of_docs",
			"label": i.allowed+" (No. of Docs)",
			"fieldtype": "Int"
		})
		columns.append({
			"fieldname": i.allowed+"_avg_days",
			"label": i.allowed+" (Avg Days)",
			"fieldtype": "Int"
		})
	return columns



def get_workflow(filters):
	return frappe.db.get_value("Workflow", {"document_type": filters.doctype, 'is_active':1})

def get_workflow_roles(workflow):
	return frappe.db.get_list("Workflow Transition", {"parent":workflow}, "distinct allowed")
