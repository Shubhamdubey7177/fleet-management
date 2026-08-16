// Copyright (c) 2026, shubham and contributors
// For license information, please see license.txt

frappe.ui.form.on("Fuel management", {
    fuel_quantity(frm) {
        calculate_total(frm);
    },

    per_liter_price(frm) {
        calculate_total(frm);
    }
});

function calculate_total(frm) {
    let quantity = frm.doc.fuel_quantity || 0;
    let price = frm.doc.per_liter_price || 0;

    let total = quantity * price;

    frm.set_value("total_price", total);
}