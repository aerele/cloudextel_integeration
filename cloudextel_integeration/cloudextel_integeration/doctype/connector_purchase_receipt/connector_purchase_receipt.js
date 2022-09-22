// Copyright (c) 2022, CloudExtel and contributors
// For license information, please see license.txt

frappe.ui.form.on('Connector Purchase Receipt', {
	refresh:function(frm){
		frm.add_custom_button(__("Create Purchase Receipt"), function(){
			if(frm.doc.sync == 1){
				frappe.msgprint('Purchase Receipt Already Created')
				return
			}
			frappe.call({
				'method': 'cloudextel_integeration.cloudextel_integeration.doctype.connector_purchase_receipt.connector_purchase_receipt.new_purchase_receipt',
				'args':{
					'purchase_receipt_id': frm.doc.name
				},
				'callback':function(res){
					if(res.message){
						frappe.msgprint("Purchase Receipt created")
					}
				}
			})
		})
	}
});
