# Copyright (c) 2026, shubham and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Trip(Document):
	def validate(self):
		vehicle_status = frappe.db.get_value("Vehicle", self.vehicle, "status")
		if vehicle_status == "In Maintenance":
			frappe.throw(f"Cannot assign a trip to {self.vehicle} — it is currently under maintenance.")

		if self.status == "Ongoing":
			frappe.db.set_value("Vehicle", self.vehicle, "status", "In Use")
			frappe.db.set_value("Driver", self.driver, "status", "On Trip")

	def on_submit(self):
		if self.status == "Completed":
			frappe.db.set_value("Vehicle", self.vehicle, "status", "Active")
			frappe.db.set_value("Driver", self.driver, "status", "Available")

@frappe.whitelist()
def mark_trip_completed(trip_name):
	doc = frappe.get_doc("Trip", trip_name)
	doc.status = "Completed"
	doc.save()
	doc.submit()
