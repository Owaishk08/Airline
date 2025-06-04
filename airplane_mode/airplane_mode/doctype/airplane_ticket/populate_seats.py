import frappe

def execute():
    planes = frappe.db.get_all("Airplane Ticket",pluck="name")
    for p in planes:
        plane = frappe.get_doc("Airplane Ticket",p)
        plane.set_seat()
        plane.save()

    frappe.db.commit()