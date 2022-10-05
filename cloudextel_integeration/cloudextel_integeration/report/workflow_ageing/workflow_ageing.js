// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Workflow Ageing"] = {
	"filters": [
		{
			"fieldname": "date",
			"label": "Date",
			"reqd": 1,
			"fieldtype": "DateRange",
			"default": [frappe.datetime.add_months(frappe.datetime.get_today(),-1), frappe.datetime.get_today()],
		},
		{
			"fieldname": "doctype",
			"label": "Doctype",
			"fieldtype": "Select",
			"options": ["Purchase Order", "Purchase Invoice", "Purchase Receipt", "Sales Order", "Sales Invoice", "Delivery Note"],
			"reqd": 1,
			// "get_query" : function(){
			// 	return {
			// 		"query": "cloudextel_integeration.cloudextel_integeration.report.workflow_ageing.workflow_ageing.get_workflow_doctype",
			// 	}
			// }
		},
		{
			"fieldname": "tat_limit",
			"label": "TAT Limit",
			"fieldtype": "Int",
			"default": 3,
			"reqd": 1
		},
		{
			"fieldname": "cost_center",
			"label": "Cost Center",
			"fieldtype": "Link",
			"options": "Cost Center",
			"reqd": 1
		},
		{
			"fieldname": "telecom_circle",
			"label": "Telecom Circle",
			"fieldtype": "Link",
			"options": "Telecom Circle",
			"reqd": 1
		},
		{
			"fieldname": "age1",
			"label": "Age 1",
			"fieldtype": "Int",
			"default": 5,
			"reqd": 1
		},
		{
			"fieldname": "age2",
			"label": "Age 2",
			"fieldtype": "Int",
			"default": 10,
			"reqd": 1
		},
		{
			"fieldname": "age3",
			"label": "Age 3",
			"fieldtype": "Int",
			"default": 15,
			"reqd": 1
		}
		// {
		// 	"fieldname": "role",
		// 	"label": "Role",
		// 	"fieldtype": "Link",
		// 	"options": "Role",
		// }
	]
};
