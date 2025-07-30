// Copyright (c) 2025, Maha Raja and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Gym Member", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on('Gym Member', {
    refresh: function(frm) {

    },

    attach_image: function(frm) {
        frm.trigger("refresh");
    }
});
