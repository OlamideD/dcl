// Copyright (c) 2019, John Vincent Fiel and contributors
// For license information, please see license.txt

frappe.ui.form.on('DCL Appraisal Entry', {
	refresh: function(frm) {
		frappe.call({

			"method": "erpnext.selling.report.address_and_contacts.address_and_contacts.get_party_addresses_and_contact",
			'freeze': true,
			'freeze_message': [__('Getting data'), __("Please wait") + "..."].join("<br>"),

			args: {

				party_type: "Customer",
				party: "Labcrest Ltd",
				party_group:"All Customer Groups"

			},

			callback: function (data) {
				console.log(data);
			}
		});
	}
});
