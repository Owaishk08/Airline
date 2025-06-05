# Copyright (c) 2025, Owaish Khan and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
	columns = [
		{
			"fieldname": "airline",
			"label": "Airline",
			"fieldtype": "Link",
			"options": "Airline"
		},
		{
			"fieldname": "total_revenue",
			"label": "Total Revenue",
			"fieldtype": "Currency",
			"options": "INR"
		}
	]
	at = frappe.get_all("Airplane Ticket",fields=["name","flight.airplane","total_amount"])
	#OUTPUT
	#[{'name': 'Nimbus-009-03-2025-0027-NAH-to-SVI-029','airplane': 'Nimbus-009','total_amount': 2000.0},
	#{'name': 'NovaFly Airways-016-03-2025-0041-AGT-to-NAH-043-1','airplane': 'NovaFly Airways-016','total_amount': 0.0},
 	# {'name': 'NovaFly Airways-016-03-2025-0041-AGT-to-NAH-056','airplane': 'NovaFly Airways-016','total_amount': 1500.0}]

	al = frappe.get_all("Airline",pluck="name")
	#OUTPUT
	#['Horizon Jetliners',
 	#'Nimbus Jetways',
 	#'AeroGlobe Airlines']

	revenue_by_airline = {}
	for l in al:
		revenue_by_airline[l]= 0
	
	# OUTPUT 
	#{'Horizon Jetliners': 0, 'Nimbus Jetways': 0, 'AeroGlobe Airlines': 0}
	
	for a in at:
		airline = frappe.get_value("Airplane", a.airplane, 'airline')
		#OUTPUT airline:Nimbus Jetways
		a['airline'] = airline
		frappe.errprint(a)
		frappe.errprint(a.airline)
		if a.airline in revenue_by_airline:
			revenue_by_airline[a.airline] += a.total_amount
		#OUTPUT
		# frappe.errprint(revenue_by_airline) {'Horizon Jetliners': 0, 'Nimbus Jetways': 2000.0, 'AeroGlobe Airlines': 630.0}

	data = [{"airline": i, "total_revenue": j} for i, j in revenue_by_airline.items()]
	frappe.errprint(data)
	chart = {
		"data": {
			"labels":[d["airline"] for d in data],
			"datasets":[{"name": "Revenue By Airline", "values": [d["total_revenue"] for d in data]}],
		},
		"type":"donut",
	}

	total_revenue = sum(d["total_revenue"] for d in data)
	summary = [
		{
			"label": "Total Revenue",
			"value": total_revenue,
			"indicator": "Green" if total_revenue > 0 else "Red"
		}
	]
	return columns,data,None,chart,summary

	