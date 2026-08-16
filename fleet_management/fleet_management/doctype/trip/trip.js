frappe.ui.form.on("Trip", {
    refresh(frm) {
        calculate_total(frm);

        if (frm.doc.docstatus === 0 && frm.doc.status !== "Completed") {
            frm.add_custom_button("Mark as Completed", () => {
                frappe.call({
                    method: "fleet_management.fleet_management.doctype.trip.trip.mark_trip_completed",
                    args: {
                        trip_name: frm.doc.name
                    },
                    callback: () => {
                        frm.reload_doc();
                    }
                });
            });
        }
    }
});


frappe.ui.form.on("Trip Expense", {
    amount(frm, cdt, cdn) {
        calculate_total(frm);
    }
});


function calculate_total(frm) {

    let amount = 0;

    for (let row of frm.doc.trip_expenses || []) {
        amount += row.amount || 0;
    }

    frm.set_value("total_expense", amount);
}