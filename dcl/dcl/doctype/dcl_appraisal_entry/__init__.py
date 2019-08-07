import frappe

@frappe.whitelist()
def get_kpi(template):
    return frappe.db.sql("""SELECT tasks,kpi,section FROM `tabDCL Appraisal KPI` WHERE parent=%s ORDER BY idx""",(template),as_dict=True)


@frappe.whitelist()
def get_topics(template):
    return frappe.db.sql("""SELECT topic FROM `tabDCL Appraisal Remarks` WHERE parent=%s""",(template),as_dict=True)