#!/usr/bin/python
import json
import os
import time
from pprint import pprint
from string import Template
from collections import OrderedDict

# Global variables
imgList = []
bootstrapGridL = "col-md-"
bootstrapGridM = "col-sm-"
bootstrapGridS = "col-xs-"

print "Hello, Python!"

#<!-- Place this tag where you want the button to render. -->
#<iframe src="https://ghbtns.com/github-btn.html?user=NativeScript&repo=NativeScript&type=star&count=true&size=small" frameborder="0" scrolling="0" width="160px" height="30px"></iframe>

# Format the name to lowercase and without special characters
def formatString( str ):
    output = str.replace('/','').replace(' ', '').replace('-','').replace('.','')
    return output.lower()

# Format the name to lowercase and without special characters
def checkLogoAvailability( str ):
    if str in imgList:
        return str
    else:
        return "notfound"

# Filter value to exlude true
def filterValue( str ):
    if "true" not in str:
        return str
    else:
        return ""

def constructPopularity( framework ):
    name = ""
    content = """<div class="row">"""
    value = framework.get("twitter")
    if value != "EMPTY" and value !="UNDEF":
        name = value.split("https://twitter.com/",1)[1]
        content += """<div class=\"""" + bootstrapGridS + """4 centered left"><a href=\"""" + value + """\" target="_blank"><i id=\"twitter-""" + name.lower() +"""\"class="fa fa-twitter" aria-hidden="true"></i><span class="twitter-label">0000</span></a></div>"""
    else:
        content += """<div class=\"""" + bootstrapGridS + """4 centered left"><i class="fa fa-twitter" aria-hidden="true"></i><span class="twitter-label">n/a</span></div>"""

    value = framework.get("repo")
    if value != "EMPTY" and value !="UNDEF" and value !="false":
        name = value.split("github.com/",1)[1]
        name = name.split("/",1)[0] #get the first value = the user name
        content += """<div class=\"""" + bootstrapGridS + """4 centered"><a href=\"""" + value + """\" target="_blank"><i id=\"github-""" + name.lower() +"""\"class="fa fa-github" aria-hidden="true"></i><span class="github-label">0000</span></a></div>"""
    else:
        content += """<div class=\"""" + bootstrapGridS + """4 centered"><i class="fa fa-github" aria-hidden="true"></i><span class="github-label">n/a</span></div>"""

    value = framework.get("stackoverflow")
    if value != "EMPTY" and value !="UNDEF" and value !="false":
        name = value.split("tagged/",1)[1]
        name = name.split(".",1)[0] #get name without the ".io"
        content += """<div class=\"""" + bootstrapGridS + """4 centered right"><a href=\"""" + value + """\" target="_blank"><i id=\"stackoverflow-""" + name.lower() +"""\"class="fa fa-stack-overflow" aria-hidden="true"></i><span class="stackoverflow-label">0000</span></a></div>"""
    else:
        content += """<div class=\"""" + bootstrapGridS + """4 centered right"><i class="fa fa-stack-overflow" aria-hidden="true"></i><span class="stackoverflow-label">n/a</span></div>"""

    content += """</div>"""
    return content

#Constants ----------------------
#status keywords
status = [
    "active",
    "discontinued"
]
#Technology keywords
technology = [
    "nativejavascript",
    "webtonative",
    "javascript_tool",
    "sourcecode",
    "runtime",
    "appfactory"
]
#Platform keywords
platforms = [
    "android",
    "ios",
    "windowsphone",
    "blackberry",
    "tizen",
    "firefoxos",
    "watchos"
]
#Hardware keywords
hardware = [
    "accelerometer",
    "camera",
    "capture",
    "compass",
    "connection",
    "contacts",
    "device",
    "nativeevents",
    "file",
    "geolocation",
    "notification",
    "storage",
    "gestures_multitouch",
    "messages_telephone",
    "bluetooth",
    "nfc",
    "vibration"
]
#Target keywords
target = [
    "hybridapp",
    "nativeapp",
    "mobilewebsite",
    "webapp"
]
#Development Language keywords
developmentLanguage = [
    "php",
    "basic",
    "java",
    "ruby",
    "actionscript",
    "csharp",
    "lua",
    "xml",
    "html",
    "css",
    "js",
    "cplusplus",
    "visualeditor"
]
#User Interface keywords
userInterface = [
    "cd",
    "widgets",
    "accessibility"
]
#Other features keywords
other = [
    "sdk",
    "ads",
    "encryption"
]
#Other features keywords
license = [
    "free",
    "opensource",
    "commercial",
    "enterprise"
]

# Create the filter list from the existing keyword lists
#------------------------------------------------------------
filters = [
    status,
    technology,
    platforms,
    target,
    #hardware,
    developmentLanguage,
    #userInterface,
    #other,
    license
]

filterNames = [
    "Tool status",
    "Technology",
    "Platform",
    "Target",
    #"Hardware Features",
    "Development Language",
    "License"
]

filterDesc = [
    "Is the tool still available?",
    "What cross-platform technology must be used?",
    "Which platforms must be supported by the framework?",
    "What type of application should the framework output?",
    #"Which hardware features must be supported?",
    "Which development language would you like to use?",
    "What license is required?"
]
#------------------------------------------------------------

#Footer keywords
footerLeft = {
    "url",
    "documentation_url",
    "tutorial_url"
}
footerRight = {
    "video_url",
    "book",
    "license"
}

formatKey = {
    "all": "Show All",
    "active":"Active",
    "discontinued":"Discontinued",

    "nativejavascript": "Native JavaScript",
    "webtonative": "Web-to-native wrapper",
    "javascript_tool": "JS framework/toolkit",
    "sourcecode": "Code translator",
    "runtime": "Runtime",
    "appfactory": "App Factory",

    "hybridapp":"Hybrid App",
    "nativeapp":"Native App",
    "mobilewebsite":"Mobile website",
    "webapp":"Web App",

    "ios":"iOS",
    "android":"Android",
    "wup":"Windows10",
    "windowsphone":"WindowsPhone",
    "watchos": "Watch OS",
    "tizen": "Tizen",
    "firefoxos": "Firefox OS",
    "blackberry": "Blackberry",
    "appletv": "Apple TV",
    "androidtv": "Android TV",
    "bada":"Bada",
    "osx":"OSX",
    "windows":"Windows",
    "symbian":"Symbian",
    "webos":"WebOS",

    "php":"PHP",
    "basic": "Basic",
    "java":"Java",
    "ruby":"Ruby",
    "actionscript":"ActionScript",
    "csharp":"C#",
    "lua":"LUA",
    "html":"HTML",
    "css":"CSS",
    "js":"JavaScript",
    "cplusplus":"C++",
    "xml": "XML",
    "visualeditor":"Visual Editor",

    "accelerometer":"Accelerometer",
    "camera":"Camera",
    "capture":"Capture",
    "compass":"Compass",
    "connection":"Connection",
    "contacts":"Contact",
    "device":"Device",
    "nativeevents":"Native Events",
    "file":"File",
    "geolocation":"Geolocation",
    "notification":"Notification",
    "storage":"Storage",
    "gestures_multitouch":"Gestures & Multitouch",
    "messages_telephone":"Messages & Telephone",
    "bluetooth":"Bluetooth",
    "nfc":"NFC",
    "vibration":"Vibration",

    "cd":"Corporate Design",
    "widgets":"Widgets",
    "accessibility":"Accessibility",

    "sdk":"SDK",
    "encryption":"Encryption",
    "ads":"Ads",

    "free":"Free",
    "opensource":"Open Source",
    "commercial":"Commercial lic.",
    "enterprise":"Enterprise Lic.",

    "url": "Official Website",
    "documentation_url": "Official Docs",
    "tutorial_url": "Tutorial",

    "video_url": "Video Introduction",
    "book": "Recommended Book",
    "license": "License"
}

# Read the contents of the json file
with open('frameworks.json') as data_file:
    frameworks = json.load(data_file)
numOfElements = len(frameworks)

# Format number of frameworks to "0000"
formattedNum = str(numOfElements).zfill(4)
print "Formatted number of frameworks= " + str(formattedNum)

# Create the filter checkboxes from the above lists
numOfFilters = len(filters)
print "Number of filters= " + str(numOfFilters)
filterContent = """<div class="track-tool">
    \t<h4>Number of tracked tools</h4>
    \t<div class="track-tool-nr">
	\t\t<span class="label label-default nr">""" + formattedNum[:1] + """</span>
	\t\t<span class="label label-default nr">""" + formattedNum[1:2] + """</span>
	\t\t<span class="label label-default nr">""" + formattedNum[2:3] + """</span>
	\t\t<span class="label label-default nr">""" + formattedNum[-1:] + """</span>
	\t</div>
	</div><button type="button" class="btn btn-default btn-clear" disabled>
    \tClear All<span class="glyphicon glyphicon-trash pull-right"/>
  	</button>
    """

for i in range(0, numOfFilters):
    #Panel header
    filterContent+= str("""<div class="panel-group filter-box">
    \t<div class="panel panel-default">
    \t\t<h4 class="panel-title">
    \t\t\t<a data-toggle="collapse" aria-expanded="false" href="#collapse""" + str(i) + """\">
    \t\t\t\t<div class="panel-heading">
    \t\t\t\t\t""" + filterNames[i] + """
    \t\t\t\t</div>
    \t\t\t</a>
    \t\t</h4>
    """)
    if i < 3:
        filterContent+= str("""\t\t<div id="collapse""" + str(i) + """\" class="panel-collapse collapse in">""")
    else:
        filterContent+= str("""\t\t<div id="collapse""" + str(i) + """\" class="panel-collapse collapse">""")
    filterContent+= str("""
    \t\t\t<div class="panel-body">
    \t\t\t\t<fieldset class="fieldset accordion-content" role="tab-panel" style="display: block;" aria-hidden="false">
    \t\t\t\t\t<p>""" + filterDesc[i] + """</p>
    """)
    #Create filterboxes
    for item in filters[i]:
        filterContent+= str("""\t\t\t\t\t<input id=\"""" + item + """\" type="checkbox" value=\"""" + item + """\" class="custom-checkbox"/>
        \t\t\t\t\t<label for=\"""" + item +"""\" class="checkbox-label">""" + str(formatKey.get(item)) + """</label>
        """)
    filterContent+= str("""\t\t\t\t</fieldset>
    \t\t\t</div>
    \t\t</div>
    \t</div>
    </div>
    """)

# Create list with imageNames from existing logos in folder "../img/logos/"
for path, dirs, files in os.walk("../img/logos"):
  for f in files:
    imgList.append(f[:-4])  #strip ".png" from logo names

# Construct the dynamic content string from the json input file
content = ""
urls = ["#"]
url = ""
for i in range(0, numOfElements):
    urls = ["#"]
    url = frameworks[i].get('url')
    if "|" in url:
        urls = url.split("|")
    elif url == "false" or url == "none" or url == "EMPTY" or url == "UNDEF":
        urls[0] = "#"
    else:
        urls[0] = url
    #Start panel group
    content+= str("""<div class=\"""" + bootstrapGridL + """4 """ + bootstrapGridS + """6 framework">
    \t<div class="thumbnail">
    """)
    if urls[0] == "#":
        content+= str("""\t\t<img src="img/logos/""" + checkLogoAvailability(formatString(frameworks[i].get('framework'))) + """.png" alt="">""")
    else:
        content+= str("""\t\t<a href=\"""" + str(urls[0]) + """\" target="_blank"><img src="img/logos/""" + checkLogoAvailability(formatString(frameworks[i].get('framework'))) + """.png" alt=""></a>""")
    content+= str("""\t\t<div class="caption">
    \t\t\t<h4 class="thumb-caption">""" + frameworks[i].get('framework') + """</h4>
    """)
    #Fill in technology
    content+= str("""\t\t\t<span class="info-label """)
    for key, value in frameworks[i].iteritems():
        if key in technology and value and value != "none" and value != "false" and value != "UNDEF" and value != "EMPTY":
            content+= str(key) + " "
    content+= str("""\">""")
    for key, value in frameworks[i].iteritems():
        if key in technology and value and value != "none" and value != "false" and value != "UNDEF" and value != "EMPTY":
            content+= str(formatKey.get(key)) + " + "
    content = content[:-2]  #strip last "+ " from string
    content+= """</span>\n"""
	#Fill in CPT status
    for key, value in frameworks[i].iteritems():
        if (str(value) == "Active" or str(value) == "Discontinued") and value and value != "none" and value != "false" and value != "UNDEF" and value != "EMPTY":
            content+= """\t\t\t<span class="info-label """ + str(key) + " " + str(value).lower() + """\">""" + str(value) + """</span>\n"""
    #Add Popularity numbers
    content+= constructPopularity(frameworks[i])
    #Add compare button and link
    content+= str("""\t\t\t<input id="compare-""" + str(formatString(frameworks[i].get('framework'))) + """\" type="checkbox" value="compare" class="custom-checkbox compare-checkbox"/>
    \t\t\t<label for="compare-""" + str(formatString(frameworks[i].get('framework'))) + """\" class="checkbox-label compare-label">Compare</label>
	\t\t\t<a class="btn btn-danger btn-xs compare-link hidden" href="html/compare.html" role="button">Go to compare</a>
    """)
    content+= str("""\t\t\t<div>
    \t\t\t\t<h4 class="panel-title">
    \t\t\t\t\t<a data-toggle="collapse" aria-expanded="false" href="#collapse""" + str(i+numOfFilters) + """\">
    \t\t\t\t\t\t<div class="panel-heading feature-panel">
    \t\t\t\t\t\t\t<span class="dropIcon glyphicon glyphicon-chevron-up"></span>
	\t\t\t\t\t\t\t<span class="dropIcon glyphicon glyphicon-chevron-down"></span>
    \t\t\t\t\t\t</div>
	\t\t\t\t\t</a>
	\t\t\t\t</h4>
    \t\t\t\t<div id="collapse""" + str(i+numOfFilters) + """\" class="panel-collapse collapse">
    \t\t\t\t\t<div>
	\t\t\t\t\t\t<div class="row">
	""")
    #Fill in platform
    content+= str("""\t\t\t\t\t\t\t<div class=\"""" + bootstrapGridM + """6">
    \t\t\t\t\t\t\t\t<h4 class="featureTitle">Platform</h4>
    """)
    for key, value in frameworks[i].iteritems():
        if key in platforms and value and value != "none" and value != "false" and value != "UNDEF" and value != "EMPTY":
            content+= """\t\t\t\t\t\t\t<span class="feature """ + str(key) + " " + filterValue(str(value)) + """\">""" + str(formatKey.get(key)) + """</span>\n"""
    #Fill in target
    content+= str("""\t\t\t\t\t\t\t</div>
    \t\t\t\t\t\t\t<div class=\"""" + bootstrapGridM + """6">
    \t\t\t\t\t\t\t\t<h4 class="featureTitle">Target</h4>
    """)
    for key, value in frameworks[i].iteritems():
        if key in target and value and value != "none" and value != "false" and value != "UNDEF" and value != "EMPTY":
            content+= """\t\t\t\t\t\t\t\t<span class="feature """ + str(key) + " " + filterValue(str(value)) + """\">""" + str(formatKey.get(key)) + """</span>\n"""
    #Fill in Development Language
    content+= str("""\t\t\t\t\t\t\t</div>
    \t\t\t\t\t\t</div>
    \t\t\t\t\t\t<div class="row">
    \t\t\t\t\t\t\t<div class=\"""" + bootstrapGridM + """6">
    \t\t\t\t\t\t\t\t<h4 class="featureTitle">Development Language</h4>
    """)
    for key, value in frameworks[i].iteritems():
        if key in developmentLanguage and value and value != "none" and value != "false" and value != "UNDEF" and value != "EMPTY":
            content+= """\t\t\t\t\t\t\t\t<span class="feature """ + str(key) + " " + filterValue(str(value)) + """\">""" + str(formatKey.get(key)) + """</span>\n"""
    #Fill in Terms of license
    content+= str("""\t\t\t\t\t\t\t\t</div>
    \t\t\t\t\t\t\t<div class=\"""" + bootstrapGridM + """6">
    \t\t\t\t\t\t\t\t<h4 class="featureTitle">Terms of a License</h4>
    """)
    for key, value in frameworks[i].iteritems():
        if key in license and value and value != "none" and value != "false" and value != "UNDEF" and value != "EMPTY":
            content+= """\t\t\t\t\t\t\t\t<span class="feature """ + str(key) + " " + filterValue(str(value)) + """\">""" + str(formatKey.get(key)) + """</span>\n"""
        elif key == "license":
            if "commercial" in value:
                content+= """\t\t\t\t\t\t\t\t<span class="feature commercial"\">""" + str(formatKey.get("commercial")) + """</span>\n"""
            if "enterprise" in value:
                content+= """\t\t\t\t\t\t\t\t<span class="feature enterprise"\">""" + str(formatKey.get("enterprise")) + """</span>\n"""
    #Add finish
    content+= str("""\t\t\t\t\t\t\t</div>
    \t\t\t\t\t\t</div>
    \t\t\t\t\t</div>
    \t\t\t\t</div>
    \t\t\t</div>
    \t\t</div>
    \t</div>
    </div>
    """)

#print content

placeholder1 = """<div class=\"""" + bootstrapGridM + """3 filters">"""
placeholder2 = """<div class=\"""" + bootstrapGridM + """9">
<div id="msgInfoCompare" class="alert alert-warning fade in" hidden>
    <a href="#" class="close" data-hide="alert" aria-label="close">&times;</a>
    <strong>Info!</strong> You can only select up to 5 frameworks for comparison.
</div>"""

with open('index_template.html', 'r+') as orginal, open('index.html', 'w') as output:
    for line in orginal:
        if 'col-md-3 placeholder' in line:
            output.write(placeholder1)
            output.write(filterContent)
        elif 'col-md-9 placeholder' in line:
            output.write(placeholder2)
            output.write(content)
        else:
            output.write(line)

#Move generated file and create backup of original
if os.path.isfile("../index.html"):
    print "file found " + "index.html"
    os.rename("../index.html", ("../index_org" + time.strftime("-%d_%m_%y-%H_%M") + ".html"))
    print "Create backup index.html"
    os.rename("./index.html", "../index.html")
    print "moved new file"
    
print "END"
