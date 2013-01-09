# coding=utf-8

from random import randint
from urllib import urlencode
from urllib2 import urlopen
from urlparse import urlunparse
from hashlib import sha1
from os import environ
import random

# Set your proprty id via the environment or simply type it
# below
PROPERTY_ID = environ.get("GA_PROPERTY_ID", "UA-36800415-1")
 
# Generate the visitor identifier somehow. I get it from the
# environment, calculate the SHA1 sum of it, convert this from base 16
# to base 10 and get first 10 digits of this number.
VISITOR = environ.get("GA_VISITOR", "xxxxx")
VISITOR = str(int("0x%s" % sha1(VISITOR).hexdigest(), 0))[:10]
VISITOR1 = str(int("0x%s" % sha1(VISITOR).hexdigest(), 0))[:10]
VISITOR2 = str(int("0x%s" % sha1(VISITOR).hexdigest(), 0))[:10]
VISITOR3 = str(int("0x%s" % sha1(VISITOR).hexdigest(), 0))[:10]
VISITOR4 = str(int("0x%s" % sha1(VISITOR).hexdigest(), 0))[:10]
VISITOR5 = str(int("0x%s" % sha1(VISITOR).hexdigest(), 0))[:10]
 
# The path to visit
PATH = "/inflate/some/"
HOST = "www.bloggingwithjonchow.com"
REFERRALURL = "http://www.yahoo.com?q=blogging"


resolutions=["1024×768","1280×800","1280×1024","1440×900","1680×1050"]
languages=["en-us","de","ja","ko","pt-br"]
Screencolordepth=["24-bit", "32-bit"]
#Language encoding for the browser
encoding=["UTF-8","ISO-8859-1","-"]
flash=["11.5 r31","10.0 r2","10.0 r1","9.0 r12"]

PAGETITLE="Blogging with Jon Chow"

# Collect everything in a dictionary
DATA = {"utmwv": "5.3.8",
		"utms" : "1",
        "utmn" : str(randint(1, 9999999999)),
        "utmhn": HOST,
        "utmcs": random.choice(encoding),
        "utmsr": random.choice(resolutions),
        "utmsc": random.choice(Screencolordepth),
        "utmul": random.choice(languages),        
        "utmr" : REFERRALURL,
        "utmje": "1",
        "utmfl": random.choice(flash),
        "utmdt": PAGETITLE,
        "utmp" : PATH,
        "utmac": PROPERTY_ID,
        "utmcn": "1",
        "utmcc": "__utma=%s;" % ".".join([VISITOR1, VISITOR, VISITOR2, VISITOR3, VISITOR4, "1"])}
 
# Encode this data and generate the final URL
URL = urlunparse(("http",
                  "www.google-analytics.com",
                  "/__utm.gif",
                  "",
                  urlencode(DATA),
                  ""))

# Make the request
print "Requesting", URL
print urlopen(URL).info()