import frappe
from dcl.tradegecko.tradegecko import TradeGeckoRestClient
from frappe.model.rename_doc import rename_doc
from erpnext.selling.doctype.sales_order.sales_order import make_sales_invoice as make_purchase_invoice,make_delivery_note
from dcl.inflow_import import make_payment_request
from erpnext.accounts.doctype.payment_request.payment_request import make_payment_entry
from dcl.inflow_import.stock import make_stock_entry
from dateutil import parser
from datetime import timedelta

# bench --site dcl2 execute dcl.tradegecko.contacts.get_company
def get_company(page=1,replace=0,order_number="", skip_orders=[]):
    access_token = "6daee46c0b4dbca8baac12dbb0e8b68e93934608c510bb41a770bbbd8c8a7ca5"
    refresh_token = "76098f0a7f66233fe97f160980eae15a9a7007a5f5b7b641f211748d58e583ea"
    # tg = TradeGeckoRestClient(access_token, refresh_token)
    tg = TradeGeckoRestClient(access_token)
    # print tg.company.all()['companies'][0]
    # if not order_number:

    orders = tg.company.all(page=1,limit=10)['companies']

    # else:
    #     orders = tg.order.filter(order_number=order_number)['orders']
    # print orders

    # print orders

    # supplier_company = tg.company.get(o['company_id'])['company']
    # print supplier_company

    # CREATE SUPPLIER IF NOT EXISTS
    for supplier_company in orders:
        _type = ""
        # if supplier_company['company_type'] == 'business': #supplier or business
        #     continue
        if supplier_company['contact_ids'] == []:
            continue
        print supplier_company
        if supplier_company['company_type'] == 'business':
            _type = "Customer"
        elif supplier_company['company_type'] == 'supplier':
            _type = "Supplier"

        if _type:
            customer_name = ""
            exists_supplier = frappe.db.sql("""SELECT Count(*),name FROM `tab"""+_type+"""` WHERE name=%s""",
                                            (supplier_company['name']))
            if exists_supplier[0][0] == 0:
                if _type == "Customer":
                    new_cust = frappe.get_doc({"doctype": "Customer", "customer_name": supplier_company['name'],
                                    "customer_group": "All Customer Groups", "customer_type": "Company",
                                    "account_manager": "Dummy"})
                else:
                    new_cust = frappe.get_doc({"doctype": "Supplier", "supplier_name": supplier_company['name'],
                            "supplier_group": "All Supplier Groups", "supplier_type": "Company"})
                new_cust.insert()
                frappe.db.commit()
                customer_name = new_cust.name
            else:
                customer_name = exists_supplier[0][1]
                print "exists"

            print supplier_company['address_ids']
            print supplier_company['id']
            addresses = tg.address.filter(company_id=supplier_company['id'])
            # print addresses
            for address in addresses['addresses']:
                print address
                exists_supplier = frappe.db.sql("""SELECT Count(*)
                                      FROM `tabAddress`
                                      INNER JOIN `tabDynamic Link`
                                      ON `tabDynamic Link`.parent=`tabAddress`.name
                                      WHERE address_line1=%s""",
                                                (address['address1']))
                if exists_supplier[0][0] == 0:
                    addr = frappe.get_doc({"doctype": "Address",
                                    "phone": address['phone_number'],
                                    "city": address['city'] or "Accra",
                                    "address_line1": address['address1'],
                                    "address_line2": address['address2'],
                                    "pincode": address['zip_code'],
                                    "country": address['country'],
                                    "email_id":address['email'],
                                    "links":[
                                        {
                                            "link_doctype":_type,
                                            "link_name":customer_name
                                        }
                                    ]
                                    })
                    # try:
                    addr.insert()
                    frappe.db.commit()
                    # except Exception as e:
                    #     print e
                else:
                    print "exists address"

            addresses = tg.contact.filter(company_id=supplier_company['id'])
            # print addresses
            for address in addresses['contacts']:
                print address
                exists_supplier = frappe.db.sql("""SELECT Count(*)
                                                    FROM `tabContact`
                                                    INNER JOIN `tabDynamic Link`
                                                    ON `tabDynamic Link`.parent=`tabContact`.name
                                                    WHERE first_name=%s""",
                                                (address['first_name']))
                if exists_supplier[0][0] == 0:
                    addr = frappe.get_doc({"doctype": "Contact",
                                           "phone": address['phone'],
                                           "mobile_no": address['mobile'],
                                           "first_name": address['first_name'],
                                           "last_name": address['last_name'],
                                           "email_id": address['email'],
                                           "links": [
                                               {
                                                   "link_doctype": _type,
                                                   "link_name": customer_name
                                               }
                                           ]
                                           })
                    # try:
                    addr.insert()
                    frappe.db.commit()
                    # except Exception as e:
                    #     print e
                else:
                    print "exists address"