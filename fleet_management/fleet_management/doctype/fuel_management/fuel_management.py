# Copyright (c) 2026, shubham and contributors
# For license information, please see license.txt
import frappe
from frappe.model.document import Document


class Fuelmanagement(Document):
    def validate(self):
        if self.fuel_quantity <= 0:
            frappe.throw("Fuel Quantity must be greater than zero.")

        if self.per_liter_price <= 0:
            frappe.throw("Per Liter Price must be greater than zero.")

        if self.odometer_reading < 0:
            frappe.throw("Odometer Reading cannot be negative.")
        self.total_price = self.fuel_quantity * self.per_liter_price
