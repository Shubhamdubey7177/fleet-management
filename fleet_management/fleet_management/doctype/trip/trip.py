# Copyright (c) 2026, shubham and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Trip(Document):

    def validate(self):
        if self.status == "Scheduled":

            # Vehicle validation
            vehicle_doc = frappe.get_doc("Vehicle", self.vehicle)

            if vehicle_doc.status == "In Maintenance":
                frappe.throw(
                    f"Cannot assign a trip to {self.vehicle} — "
                    "it is currently under maintenance."
                )

            if vehicle_doc.status == "Active":
                frappe.throw(
                    f"Cannot assign a trip to {self.vehicle} — "
                    "it is currently in use."
                )

            # Driver validation
            driver_doc = frappe.get_doc("Driver", self.driver)

            if driver_doc.status == "On Trip":
                frappe.throw(
                    f"Cannot assign a trip to {self.driver} — "
                    "it is currently on trip."
                )

            if driver_doc.status == "Off Duty":
                frappe.throw(
                    f"Cannot assign a trip to {self.driver} — "
                    "Driver is Off Duty"
                )



        if self.start_date is not None and self.end_date is not None:

            if self.start_date > self.end_date:
                frappe.throw(
                    f"Cannot assign a trip to {self.driver} — "
                    "start date cannot be ahead of end date"
                )



        if self.distance_km is not None and self.distance_km <= 0:
            frappe.throw(
                "Distance cannot be negative or equal to zero"
            )



        for row in self.trip_expenses:

            if row.amount is not None and row.amount <= 0:
                frappe.throw(
                    "Amount should be greater than zero"
                )



    def on_update(self):

        if self.has_value_changed("status"):

            if self.status == "Ongoing":

                frappe.db.set_value(
                    "Vehicle",
                    self.vehicle,
                    "status",
                    "Active"
                )

                frappe.db.set_value(
                    "Driver",
                    self.driver,
                    "status",
                    "On Trip"
                )



    def on_submit(self):

        if self.status == "Completed":

            frappe.db.set_value(
                "Vehicle",
                self.vehicle,
                "status",
                "Inactive"
            )

            frappe.db.set_value(
                "Driver",
                self.driver,
                "status",
                "Available"
            )




@frappe.whitelist()
def mark_trip_completed(trip_name):

    trip_doc = frappe.get_doc("Trip", trip_name)

    if trip_doc.status != "Ongoing":
        frappe.throw(
            "Trip must be Ongoing before it can be completed."
        )

    trip_doc.status = "Completed"

    trip_doc.save()

    trip_doc.submit()