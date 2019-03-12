import frappe

def remove_in_words(doc,method):
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