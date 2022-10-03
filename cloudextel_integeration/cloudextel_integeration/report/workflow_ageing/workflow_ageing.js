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
			"fieldtype": "Link",
			"options": "DocType",
			"reqd": 1,
			"get_query" : function(){
				return {
					"query": "cloudextel_integeration.cloudextel_integeration.report.workflow_ageing.workflow_ageing.get_workflow_doctype",
				}
			}
		},
		// {
		// 	"fieldname": "cost_center",
		// 	"label": "Cost Center",
		// 	"fieldtype": "Link",
		// 	"options": "Cost Center",
		// },
		// {
		// 	"fieldname": "telecom_circle",
		// 	"label": "Telecom Circle",
		// 	"fieldtype": "Select",
		// 	"options": "Telecom Circle",
		// },
		// {
		// 	"fieldname": "role",
		// 	"label": "Role",
		// 	"fieldtype": "Link",
		// 	"options": "Role",
		// }
	]
};
