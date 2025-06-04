# Copyright (c) 2025, Owaish Khan and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
	columns = [
		{
			"fieldname": "airplane",
			"label": "Airplane",
			"fieldtype": "Data"
		},
		{
			"fieldname": "total_revenue",
			"label": "Total Revenue",
			"fieldtype": "Currency",
		}
	]
	
	data = frappe.get_all(
		"Airplane Ticket", 
		filters={"docstatus":1}, 
		fields=["flight.airplane","SUM(total_amount) AS total_revenue"],
		group_by="flight"
	)

	chart = {
		"data": {
			"labels":[x.airplane for x in data],
			"datasets":[{"values":[x.total_revenue for x in data]}],
		},
		"type":"donut",
	}
	return columns, data,"Here is the Report", chart