frappe.ui.form.on("Trip", {
	refresh(frm) {
		// Only show this button if the trip is still a Draft (not yet submitted)
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
	},
});
