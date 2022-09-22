// Copyright (c) 2022, CloudExtel and contributors
// For license information, please see license.txt

frappe.ui.form.on('Connector Stock Entry', {
	refresh:function(frm){
		frm.add_custom_button(__("Create Stock Entry"), function(){
			if(frm.doc.sync == 1){
				frappe.msgprint('Stock Entry Already Created')
				return
			}
			frappe.call({
				'method': 'cloudextel_integeration.cloudextel_integeration.doctype.connector_stock_entry.connector_stock_entry.new_stock_entry',
				'args':{
					'name': frm.doc.name
				},
				'callback':function(res){
					if(res.message){
						frappe.msgprint("Stock Entry created")
					}
				}
			})
		})
	}
});
