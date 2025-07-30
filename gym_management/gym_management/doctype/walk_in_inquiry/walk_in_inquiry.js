// Copyright (c) 2025, Maha Raja and contributors
// For license information, please see license.txt

frappe.ui.form.on("Walk-In Inquiry", {
	refresh(frm) {
        if (frm.doc.status === 'Converted' && frm.doc.docstatus === 0) {
            frm.add_custom_button('Create Gym Member', () => {
                frappe.new_doc('Gym Member', {
                    full_name: frm.doc.visitor_name,
                    contact_number: frm.doc.contact_number,
                    email_id: frm.doc.email,
                    branch: frm.doc.branch
                });
            });
        }
	},
});

