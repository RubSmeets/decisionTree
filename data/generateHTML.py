#!/usr/bin/python
import json
import os
import time
from pprint import pprint
from string import Template
from collections import OrderedDict

# Global variables
imgList = []

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
    "javascript",
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
    "opensource"
]

# Create the filter list from the existing keyword lists
#------------------------------------------------------------
filters = [
    status,
    technology,
    platforms,
    target,
    hardware,
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
    "Hardware Features",
    "Development Language",
    "License"
]

filterDesc = [
    "Is the tool still available?",
    "What cross-platform technology must be used?",
    "Which platforms must be supported by the framework?",
    "What type of application should the framework output?",
    "Which hardware features must be supported?",
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
    "javascript": "JS framework/toolkit",
    "sourcecode": "Source-code translator",
    "runtime": "Runtime",
    "appfactory": "App Factory",

    "hybridapp":"Hybrid App",
    "nativeapp":"Native App",
    "mobilewebsite":"Mobile website",
    "webapp":"Web App",

    "ios":"iOS",
    "android":"Android",
    "windowsphone":"WindowsPhone",
    "watchos": "Watch OS",
    "tizen": "Tizen",
    "firefoxos": "Firefox OS",
    "blackberry": "Blackberry",

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

    "url": "Official Website",
    "documentation_url": "Official Docs",
    "tutorial_url": "Tutorial",

    "video_url": "Video Introduction",
    "book": "Recommended Book",
    "license": "License"
}


# Create the filter checkboxes from the above lists
numOfFilters = len(filters)
print "Number of filters= " + str(numOfFilters)
filterContent = """<button type="button" class="btn btn-default btn-clear" disabled>
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
        filterContent+= str("""\t\t\t\t\t<input id=\"""" + item + """\" type="checkbox" value=\"""" + item + """\" class="filter-checkbox"/>
        \t\t\t\t\t<label for=\"""" + item +"""\" class="filter-label">""" + str(formatKey.get(item)) + """</label>
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

# Read the contents of the json file
with open('frameworks.json') as data_file:
    frameworks = json.load(data_file)

# Construct the dynamic content string from the json input file
numOfElements = len(frameworks)
content = ""
for i in range(0, numOfElements):
    #Start panel group
    content+= str("""<div class="col-md-4 framework">
    \t<div class="thumbnail">
    \t\t<img src="img/logos/""" + checkLogoAvailability(formatString(frameworks[i].get('framework'))) + """.png" alt="">
    \t\t<div class="caption">
    \t\t\t<h4 class="thumb-caption">""" + frameworks[i].get('framework') + """</h4>
    """)
    #Fill in technology
    content+= str("""\t\t\t<span class="info-label """)
    for key, value in frameworks[i].iteritems():
        if key in technology and value and value != "none" and value != "false":
            content+= str(key) + " "
    content+= str("""\">""")
    for key, value in frameworks[i].iteritems():
        if key in technology and value and value != "none" and value != "false":
            content+= str(formatKey.get(key)) + " + "
    content = content[:-2]  #strip last "+ " from string
    content+= """</span>\n"""
	#Fill in CPT status
    for key, value in frameworks[i].iteritems():
        if (str(value) == "Active" or str(value) == "Discontinued") and value and value != "none" and value != "false":
            content+= """\t\t\t<span class="info-label """ + str(key) + " " + str(value).lower() + """\">""" + str(value) + """</span>\n"""
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
    content+= str("""\t\t\t\t\t\t\t<div class="col-md-6">
    \t\t\t\t\t\t\t\t<h4 class="featureTitle">Platform</h4>
    """)
    for key, value in frameworks[i].iteritems():
        if key in platforms and value and value != "none" and value != "false":
            content+= """\t\t\t\t\t\t\t<span class="feature """ + str(key) + " " + str(value) + """\">""" + str(formatKey.get(key)) + """</span>\n"""
    #Fill in target
    content+= str("""\t\t\t\t\t\t\t</div>
    \t\t\t\t\t\t\t<div class="col-md-6">
    \t\t\t\t\t\t\t\t<h4 class="featureTitle">Target</h4>
    """)
    for key, value in frameworks[i].iteritems():
        if key in target and value and value != "none" and value != "false":
            content+= """\t\t\t\t\t\t\t\t<span class="feature """ + str(key) + " " + str(value) + """\">""" + str(formatKey.get(key)) + """</span>\n"""
    #Fill in Development Language
    content+= str("""\t\t\t\t\t\t\t</div>
    \t\t\t\t\t\t</div>
    \t\t\t\t\t\t<div class="row">
    \t\t\t\t\t\t\t<div class="col-md-6">
    \t\t\t\t\t\t\t\t<h4 class="featureTitle">Development Language</h4>
    """)
    for key, value in frameworks[i].iteritems():
        if key in developmentLanguage and value and value != "none" and value != "false":
            content+= """\t\t\t\t\t\t\t\t<span class="feature """ + str(key) + " " + str(value) + """\">""" + str(formatKey.get(key)) + """</span>\n"""
    #Fill in Terms of license
    content+= str("""\t\t\t\t\t\t\t\t</div>
    \t\t\t\t\t\t\t<div class="col-md-6">
    \t\t\t\t\t\t\t\t<h4 class="featureTitle">Terms of a License</h4>
    """)
    for key, value in frameworks[i].iteritems():
        if key in license and value and value != "none" and value != "false":
            content+= """\t\t\t\t\t\t\t\t<span class="feature """ + str(key) + " " + str(value) + """\">""" + str(formatKey.get(key)) + """</span>\n"""
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

print content

placeholder1 = """<div class="col-md-3 filters">"""
placeholder2 = """<div class="col-md-9">"""

with open('indexCopy.html', 'r+') as orginal, open('index.html', 'w') as output:
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
