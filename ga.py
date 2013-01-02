"""
Simple proof of concept code to push data to Google Analytics.
 
Related blog post: http://www.canb.net/2012/01/push-data-to-google-analytics-with.html
"""
from random import randint
from urllib import urlencode
from urllib2 import urlopen
from urlparse import urlunparse
from hashlib import sha1
from os import environ
 
# Set your proprty id via the environment or simply type it
# below
PROPERTY_ID = environ.get("GA_PROPERTY_ID", "UA-36800415-1")
 
# Generate the visitor identifier somehow. I get it from the
# environment, calculate the SHA1 sum of it, convert this from base 16
# to base 10 and get first 10 digits of this number.
VISITOR = environ.get("GA_VISITOR", "xxxxx")
VISITOR = str(int("0x%s" % sha1(VISITOR).hexdigest(), 0))[:10]
 
# The path to visit
PATH = "/sample/path/"
 
# Collect everything in a dictionary
DATA = {"utmwv": "5.3.8",
        "utmn": str(randint(1, 9999999999)),
        "utmp": PATH,
        "utmac": PROPERTY_ID,
        "utmcc": "__utma=%s;" % ".".join(["1", VISITOR, "1", "1", "1", "1"])}
 
# Encode this data and generate the final URL
URL = urlunparse(("http",
                  "www.google-analytics.com",
                  "/__utm.gif",
                  "",
                  urlencode(DATA),
                  ""))
URL ="http://www.google-analytics.com/__utm.gif?utmwv=5.3.8d&utms=1&utmn=854646668&utmhn=www.bloggingwithjonchow.com&utmcs=UTF-8&utmsr=1920x1080&utmvp=1152x729&utmsc=24-bit&utmul=en-us&utmje=1&utmfl=11.5%20r31&utmdt=Blogging%20with%20Jon%20Chow&utmhid=1974888761&utmr=-&utmp=%2F&utmac=UA-36800415-1&utmcc=__utma%3D257191512.1929444390.1357108658.1357108658.1357108658.1%3B%2B__utmz%3D257191512.1357108658.1.1.utmcsr%3D(direct)%7Cutmccn%3D(direct)%7Cutmcmd%3D(none)%3B&utmu=q~ "
# Make the request
print "Requesting", URL
print urlopen(URL).info()