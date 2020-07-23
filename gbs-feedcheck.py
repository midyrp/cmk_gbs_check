#!/usr/bin/python3

##########################################################################################################################
#
# place in: /usr/lib/check_mk_agent/local
# and make executable
#
# greenbone gvm tools must be installed (check settings line 17)
#
##########################################################################################################################

import os
import sys
import datetime
import xml.etree.ElementTree as ET

feedinfo = os.popen("su gmp -c '/opt/gmp/.local/bin/gvm-cli -c \"/opt/gmp/gvm-tools.config\" ssh --hostname localhost --xml \"<get_feeds />\" '  ").read()
try:
    tree = ET.fromstring(feedinfo)
except:
    print("3 openvas_feed_NVT - Could not get feed info")
    print("3 openvas_feed_SCAP - Could not get feed info")
    print("3 openvas_feed_CERT - Could not get feed info")
    sys.exit(3)

if tree.attrib.get('status') != "200":
    print("2 openvas_feed_NVT - Failed to get feed info")
    print("2 openvas_feed_SCAP - Failed to get feed info")
    print("2 openvas_feed_CERT - Failed to get feed info")
    sys.exit(2)

for feedlist in list(tree):
    feedtype=""
    feedversion=""
    for securityfeed in list(feedlist):
        if securityfeed.tag.lower() == "type":
            feedtype=securityfeed.text.strip()
        if securityfeed.tag.lower() == "version":
            feedversion=securityfeed.text.strip()
        if securityfeed.tag.lower() == "name":
            feedname=securityfeed.text.strip()
    if feedtype == "":
        continue
    if feedversion=="":
        print("3 openvas_feed_" + feedtype + " - " + feedname + " Unknown date")
        continue
    if len(feedversion) != 12:
        print("3 openvas_feed_" + feedtype + " - " + feedname + " cannot interpret date " + feedversion)
        continue
    feedage=(datetime.datetime.now() - datetime.datetime(int(feedversion[:4]),int(feedversion[4:6]),int(feedversion[6:8]),int(feedversion[8:10]),int(feedversion[10:12]),0))
    feedage=int(0.5 + 24 * feedage.days + (feedage.seconds/3600))
    if feedage < 72: # three days
        print("0 openvas_feed_" + feedtype + " - " + feedname + " " + feedversion + " " + str(feedage) + " hours")
    elif feedage > 120: # five days
        print("2 openvas_feed_" + feedtype + " - " + feedname + " TO OLD " + feedversion + " " + str(feedage) + " hours")
    else:
        print("1 openvas_feed_" + feedtype + " - " + feedname + " getting old " + feedversion + " " + str(feedage) + " hours")

