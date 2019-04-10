// Copyright (c) 2019, John Vincent Fiel and contributors
// For license information, please see license.txt

frappe.ui.form.on('DCL Appraisal Entry', {
	refresh: function(frm) {

	},
	appraisal_template:function (frm) {
		if (frm.doc.appraisal_template) {
			cur_frm.doc.kpi = [];
			cur_frm.doc.remarks = [];
			frappe.call({

				"method": "dcl.dcl.doctype.dcl_appraisal_entry.get_kpi",
				'freeze': true,
				'freeze_message': [__('Getting data'), __("Please wait") + "..."].join("<br>"),

				args: {

					template: frm.doc.appraisal_template

				},

				callback: function (data) {
					console.log(data);
					for(var i=0;i<data.message.length;i++)
					{
						console.log(data.message[i]);
						var newrow = frm.add_child("kpi");
						newrow.tasks = data.message[i].tasks;
						newrow.kpi = data.message[i].kpi;
						cur_frm.refresh_field("kpi");
					}
				}
			});


				frappe.call({

				"method": "dcl.dcl.doctype.dcl_appraisal_entry.get_topics",
				'freeze': true,
				'freeze_message': [__('Getting data'), __("Please wait") + "..."].join("<br>"),

				args: {

					template: frm.doc.appraisal_template

				},

				callback: function (data) {
					console.log(data);
					for(var i=0;i<data.message.length;i++)
					{
						console.log(data.message[i]);
						var newrow = frm.add_child("remarks");
						newrow.topic = data.message[i].topic;
						cur_frm.refresh_field("remarks");
					}
				}
			});
		}
	}
});
