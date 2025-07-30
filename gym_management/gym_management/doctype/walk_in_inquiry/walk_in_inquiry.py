# Copyright (c) 2025, Maha Raja and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class WalkInInquiry(Document):
	def validate(self):
		if self.status == "Converted" and not self.email:
			frappe.throw("Email is required for conversion.")
