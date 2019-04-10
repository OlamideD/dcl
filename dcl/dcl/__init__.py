import frappe
from six import iteritems


def remove_in_words(doc, method):
    # print "##########################"
    # print "##   REMOVE IN WORDS    ##"
    # print "##########################"
    if len(doc.in_words) > 140:
        doc.in_words = ""
        doc.base_in_words = ""
        # print doc.in_words
        # print "##########################"
        # print "##         DONE         ##"
        # print "##########################"


field_map = {
    "Contact": ["first_name", "last_name", "phone", "mobile_no", "email_id", "is_primary_contact"],
    "Address": ["address_line1", "address_line2", "city", "state", "pincode", "country", "is_primary_address"]
}


def get_party_details(party_type, party_list, doctype, party_details):
    filters = [
        ["Dynamic Link", "link_doctype", "=", party_type],
        ["Dynamic Link", "link_name", "in", party_list]
    ]
    fields = ["`tabDynamic Link`.link_name"] + field_map.get(doctype, [])

    records = frappe.get_list(doctype, filters=filters, fields=fields, as_list=True)
    for d in records:
        details = party_details.get(d[0])
        details.setdefault(frappe.scrub(doctype), []).append(d[1:])

    return party_details


def add_blank_columns_for(doctype):
    return ["" for field in field_map.get(doctype, [])]


def get_party_group(party_type):
    if not party_type: return
    group = {
        "Customer": "customer_group",
        "Supplier": "supplier_group",
        "Sales Partner": "partner_type"
    }

    return group[party_type]


def get_party_addresses_and_contact(party_type, party, party_group):
    data = []
    filters = None
    party_details = frappe._dict()

    if not party_type:
        return []

    if party:
        filters = {"name": party}

    fetch_party_list = frappe.get_list(party_type, filters=filters, fields=["name", party_group], as_list=True)
    party_list = [d[0] for d in fetch_party_list]
    party_groups = {}
    for d in fetch_party_list:
        party_groups[d[0]] = d[1]

    for d in party_list:
        party_details.setdefault(d, frappe._dict())

    party_details = get_party_details(party_type, party_list, "Address", party_details)
    party_details = get_party_details(party_type, party_list, "Contact", party_details)

    for party, details in iteritems(party_details):
        addresses = details.get("address", [])
        contacts = details.get("contact", [])
        if not any([addresses, contacts]):
            result = [party]
            result.append(party_groups[party])
            result.extend(add_blank_columns_for("Contact"))
            result.extend(add_blank_columns_for("Address"))
            data.append(result)
        else:
            addresses = list(map(list, addresses))
            contacts = list(map(list, contacts))

            max_length = max(len(addresses), len(contacts))
            for idx in range(0, max_length):
                result = [party]
                result.append(party_groups[party])
                address = addresses[idx] if idx < len(addresses) else add_blank_columns_for("Address")
                contact = contacts[idx] if idx < len(contacts) else add_blank_columns_for("Contact")
                result.extend(address)
                result.extend(contact)

                data.append(result)
    return data
