// Copyright (c) 2022, CloudExtel and contributors
// For license information, please see license.txt

frappe.ui.form.on('Connector Delivery Note', {
	refresh:function(frm){
		frm.add_custom_button(__("Create Delivery Note"), function(){
			if(frm.doc.is_synced == 1){
				frappe.msgprint('Delivery Note Already Created')
				return
			}
			frappe.call({
				'method': 'cloudextel_integeration.cloudextel_integeration.doctype.connector_delivery_note.connector_delivery_note.create_dn',
				'args':{
					'name': frm.doc.name
				},
				'callback':function(res){
					if(res.message){
						frappe.msgprint("Delivery Note created")
					}
				}
			})
		})
	}
});
