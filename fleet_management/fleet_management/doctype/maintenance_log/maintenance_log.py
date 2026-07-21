# Copyright (c) 2026, shubham and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class MaintenanceLog(Document):
	def before_save(self):
		# Automatically mark the vehicle as "In Maintenance" whenever a log is created for it
		frappe.db.set_value("Vehicle", self.vehicle, "status", "In Maintenance")
