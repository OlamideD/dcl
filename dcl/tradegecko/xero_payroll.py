import frappe
# from xero.payrollmanager import PayrollManager
#
# class Payroll(object):
#     """An ORM-like interface to the Xero Payroll API"""
#
#     OBJECT_LIST = (
#         "Employees",
#         "Timesheets",
#         "PayItems",
#         "PayRuns",
#         "PayrollCalendars",
#         "Payslip",
#         "LeaveApplications",
#     )
#
#     def __init__(self, credentials, unit_price_4dps=False, user_agent=None):
#         for name in self.OBJECT_LIST:
#             setattr(self, name.lower(), PayrollManager(name, credentials, unit_price_4dps,
#                                                        user_agent))

#bench --site dcl2 execute dcl.tradegecko.xero_payroll.get_payroll
def get_payroll():
    from xero import Xero
    from xero.auth import PublicCredentials
    consumer_key = "OGCNPDYYZGJ3HVXTI2GLQDCV8HTVLG"
    consumer_secret = "OGCNPDYYZGJ3HVXTI2GLQDCV8HTVLG"
    from xero.auth import PublicCredentials
    import os
    # file = "privatekey.pem"
    # with open(os.path.dirname(os.path.abspath(__file__)) + '/data/' + file) as keyfile:
    #     rsa_key = keyfile.read()
    # print rsa_key
    credentials = PublicCredentials(consumer_key,consumer_secret)
    print credentials.url
    # xero = Xero(credentials)
    # print xero.payrollAPI.payruns.all()