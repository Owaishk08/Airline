# Copyright (c) 2025, Owaish Khan and contributors
# For license information, please see license.txt

import frappe
import random
from frappe.model.document import Document

class AirplaneTicket(Document):
	def before_save(self):
		# self.total_amount = self.flight_price * 5
		self.calculate_amount()

		items = self.add_ons
		unique_items = []
		item_codes = set()

		for row in items:
			if row.item not in item_codes:
				item_codes.add(row.item)
				unique_items.append(row)
			
		self.item = unique_items

	def calculate_amount(self):
		total_amount = 0
		if not self.add_ons:
			self.total_amount = self.flight_price
			frappe.errprint(self.total_amount)

		else:
			for add_on in self.add_ons:
				total_amount = total_amount + add_on.amount
				frappe.errprint(total_amount)

			self.total_amount = total_amount + self.flight_price
			frappe.errprint(self.total_amount)

			

	def before_submit(self):
		if self.status != 'Boarded':
			frappe.throw('The status is not equal to Boarded.')

	def before_insert(self):
		seat_col = ['A', 'B', 'C', 'D', 'E']
		self.seat = str(random.randint(1, 50)) + random.choice(seat_col)
		#self.validate_add_ons(self)
		
	def validate_add_ons(self):
		doc = frappe.get_doc("Airplane Ticket", self.name)
		dict_of_add_ons = []
		for add_on in doc.add_ons:
			frappe.errprint(add_on)
			# if add_on in dict_of_add_ons:
			# 	frappe.throw("Lead Owner cannot be same as the Lead Email Address")
			# else:
			# 	dict_of_add_ons.append(add_on.item)
	
	def validate(self):
		# Get the flight linked to this ticket
		if not self.flight:
			return

		# Get the airplane linked to the flight
		airplane = frappe.db.get_value('Airplane Flight',self.flight,'airplane')

		if not airplane:
			return
		
		# Get the capacity of the airplane
		capacity = frappe.db.get_value('Airplane',airplane,'capacity')

		# count existing tickets for this flight
		existing_tickets = frappe.db.count('Airplane Ticket',{
			'flight': self.flight,
			'docstatus': ('!=',2)
		})
		
		# check if the limit is reached
		if existing_tickets >= capacity:
			frappe.throw("Cannot create Ticket: No Seat Available.")