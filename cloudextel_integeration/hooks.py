from . import __version__ as app_version

app_name = "cloudextel_integeration"
app_title = "Cloudextel Integeration"
app_publisher = "CloudExtel"
app_description = "App to integerate ERP with WMS"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "hello@aerele.in"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/cloudextel_integeration/css/cloudextel_integeration.css"
# app_include_js = "/assets/cloudextel_integeration/js/cloudextel_integeration.js"

# include js, css files in header of web template
# web_include_css = "/assets/cloudextel_integeration/css/cloudextel_integeration.css"
# web_include_js = "/assets/cloudextel_integeration/js/cloudextel_integeration.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "cloudextel_integeration/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "cloudextel_integeration.install.before_install"
# after_install = "cloudextel_integeration.install.after_install"
after_migrate = ["cloudextel_integeration.install.after_install"]
# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "cloudextel_integeration.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Supplier":{
		"on_update": "cloudextel_integeration.integeration.supplier"
	},
	"Customer":{
		"on_update": "cloudextel_integeration.integeration.customer"
	},
	"Address":{
		"on_update": "cloudextel_integeration.integeration.address_and_contact"
	},
	"Contact":{
		"on_update": "cloudextel_integeration.integeration.address_and_contact"
	},
	"Sales Order":{
		"on_submit": "cloudextel_integeration.integeration.create_sales_order",
		"on_cancel": "cloudextel_integeration.integeration.cancel_sales_order"
	},
	"Material Request":{
		"on_submit": "cloudextel_integeration.integeration.create_material_request",
		"on_cancel": "cloudextel_integeration.integeration.cancel_sales_order"
	},
	"Purchase Order":{
		"on_submit": "cloudextel_integeration.integeration.create_purchase_order",
	},
	"Item":{
		"on_update": "cloudextel_integeration.integeration.item"
	}
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"cloudextel_integeration.tasks.all"
# 	],
# 	"daily": [
# 		"cloudextel_integeration.tasks.daily"
# 	],
# 	"hourly": [
# 		"cloudextel_integeration.tasks.hourly"
# 	],
# 	"weekly": [
# 		"cloudextel_integeration.tasks.weekly"
# 	]
# 	"monthly": [
# 		"cloudextel_integeration.tasks.monthly"
# 	]
# }

scheduler_events = {
	"cron": {
		"*/1 * * * *": [
			"cloudextel_integeration.cloudextel_integeration.doctype.connector_delivery_note.connector_delivery_note.create_delivery_note",
			"cloudextel_integeration.cloudextel_integeration.doctype.connector_stock_entry.connector_stock_entry.create_stock_entry",
			"cloudextel_integeration.cloudextel_integeration.doctype.connector_purchase_receipt.connector_purchase_receipt.create_purchase_receipt"
		]
	}
}

# Testing
# -------

# before_tests = "cloudextel_integeration.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "cloudextel_integeration.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "cloudextel_integeration.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"cloudextel_integeration.auth.validate"
# ]

