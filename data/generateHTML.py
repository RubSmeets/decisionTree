#!/usr/bin/python
import json
from pprint import pprint
from string import Template
from collections import OrderedDict

print "Hello, Python!"

#Constants ----------------------
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
    "java",
    "ruby",
    "actionscript",
    "csharp",
    "lua",
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
    platforms,
    target,
    developmentLanguage,
    userInterface,
    other,
    license
]

filterNames = [
    "Platform",
    "Target",
    "Development Language",
    "User Interface",
    "Other",
    "License"
]

filterDesc = [
    "Select which platforms must be supported by the framework",
    "What type of application should the framework output?",
    "What type of application should the framework output?",
    "What type of application should the framework output?",
    "What type of application should the framework output?",
    "What type of application should the framework output?"
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
    "java":"Java",
    "ruby":"Ruby",
    "actionscript":"ActionScript",
    "csharp":"C#",
    "lua":"LUA",
    "html":"HTML",
    "css":"CSS",
    "js":"JavaScript",
    "cplusplus":"C++",

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
filterContent = ""

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
    \t\t<div id="collapse""" + str(i) + """\" class="panel-collapse collapse">
    \t\t\t<div class="panel-body">
    \t\t\t\t<fieldset class="fieldset accordion-content" role="tab-panel" style="display: block;" aria-hidden="false">
    \t\t\t\t\t<p>""" + filterDesc[i] + """</p>
    """)
    #Create filterboxes
    for item in filters[i]:
        filterContent+= str("""\t\t\t\t\t<input type="checkbox" value=""/><label class="filterItem">""" + item + """</label>
        """)
    filterContent+= str("""\t\t\t\t</fieldset>
    \t\t\t</div>
    \t\t</div>
    \t</div>
    </div>
    """)

# Read the contents of the json file
with open('frameworks.json') as data_file:
    frameworks = json.load(data_file)

# Construct the dynamic content string from the json input file
numOfElements = len(frameworks)
content = ""
for i in range(0, numOfElements):
    #Start panel group
    content+= str("""<div class="panel-group framework">
    \t<div class="panel panel-default">
    \t\t<h4 class="panel-title">
    \t\t\t<a data-toggle="collapse" aria-expanded="false" href="#collapse""" + str(i+numOfFilters) + """\">
    \t\t\t\t<div class="panel-heading">
    \t\t\t\t\t<span class="framework-title">""" + frameworks[i].get('framework') + """</span>
    \t\t\t\t\t<span class="dropIcon pull-right glyphicon glyphicon-chevron-up"></span>
	\t\t\t\t\t<span class="dropIcon pull-right glyphicon glyphicon-chevron-down"></span>
    \t\t\t\t</div>
    \t\t\t</a>
    \t\t</h4>
    \t\t<div id="collapse""" + str(i+numOfFilters) + """\" class="panel-collapse collapse">
    \t\t\t<div class="panel-body">
    \t\t\t\t<div class="row">
    """)
    #Fill in platform
    content+= str("""\t\t\t\t\t<div class="col-md-3">
    \t\t\t\t\t\t<h4 class="featureTitle">Platform</h4>
    """)
    for key, value in frameworks[i].iteritems():
        if key in platforms and value and value != "none" and value != "false":
            content+= """\t\t\t\t\t\t<span class="feature """ + str(value) + """\">""" + str(formatKey.get(key)) + """</span>\n"""
    #Fill in target
    content+= str("""\t\t\t\t\t</div>
    \t\t\t\t\t<div class="col-md-3">
    \t\t\t\t\t\t<h4 class="featureTitle">Target</h4>
    """)
    for key, value in frameworks[i].iteritems():
        if key in target and value and value != "none" and value != "false":
            content+= """\t\t\t\t\t\t<span class="feature """ + str(value) + """\">""" + str(formatKey.get(key)) + """</span>\n"""
    #Fill in Development Language
    content+= str("""\t\t\t\t\t</div>
    \t\t\t\t\t<div class="col-md-3">
    \t\t\t\t\t\t<h4 class="featureTitle">Development Language</h4>
    """)
    for key, value in frameworks[i].iteritems():
        if key in developmentLanguage and value and value != "none" and value != "false":
            content+= """\t\t\t\t\t\t<span class="feature """ + str(value) + """\">""" + str(formatKey.get(key)) + """</span>\n"""
    #Fill in Hardware features    
    content+= str("""\t\t\t\t\t</div>
    \t\t\t\t\t<div class="col-md-3">
    \t\t\t\t\t\t<h4 class="featureTitle">Hardware</h4>
    """)
    for key, value in frameworks[i].iteritems():
        if key in hardware and value and value != "none" and value != "false":
            content+= """\t\t\t\t\t\t<span class="feature """ + str(value) + """\">""" + str(formatKey.get(key)) + """</span>\n"""
    #Start new row to wrap content and begin with User Interface
    content+= str("""\t\t\t\t\t</div>
    \t\t\t\t</div>
    \t\t\t\t<div class="row">
    \t\t\t\t\t<div class="col-md-3">
    \t\t\t\t\t\t<h4 class="featureTitle">User Interface</h4>
    """)
    for key, value in frameworks[i].iteritems():
        if key in userInterface and value and value != "none" and value != "false":
            content+= """\t\t\t\t\t\t<span class="feature """ + str(value) + """\">""" + str(formatKey.get(key)) + """</span>\n"""
    #Fill in other features
    content+= str("""\t\t\t\t\t</div>
    \t\t\t\t\t<div class="col-md-3">
    \t\t\t\t\t\t<h4 class="featureTitle">Other</h4>
    """)
    for key, value in frameworks[i].iteritems():
        if key in other and value and value != "none" and value != "false":
            content+= """\t\t\t\t\t\t<span class="feature """ + str(value) + """\">""" + str(formatKey.get(key)) + """</span>\n"""
    #Fill in Terms of license
    content+= str("""\t\t\t\t\t</div>
    \t\t\t\t\t<div class="col-md-3">
    \t\t\t\t\t\t<h4 class="featureTitle">Terms of a License</h4>
    """)
    for key, value in frameworks[i].iteritems():
        if key in license and value and value != "none" and value != "false":
            content+= """\t\t\t\t\t\t<span class="feature """ + str(value) + """\">""" + str(formatKey.get(key)) + """</span>\n"""
    #Add footer of panel group
    content+= str("""\t\t\t\t\t</div>
    \t\t\t\t</div>
    \t\t\t</div>
    \t\t\t<div class="panel-footer">
    \t\t\t\t<div class="row">
    \t\t\t\t\t<div class="col-md-6">
    """)
    for key, value in frameworks[i].iteritems():
        if key in footerLeft and value and value != "none" and value != "false":
            content+= """\t\t\t\t\t\t<a itemprop="url" href=\"""" + str(value) + """\" target="_blank">""" + str(formatKey.get(key)) + """</a>\n"""
    content+= str("""\t\t\t\t\t</div>
    \t\t\t\t\t<div class="col-md-6">
    """)
    for key, value in frameworks[i].iteritems():
        if key in footerRight and value and value != "none" and value != "false":
            content+= """\t\t\t\t\t\t<a itemprop="url" href=\"""" + str(value) + """\" target="_blank">""" + str(formatKey.get(key)) + """</a>\n"""
    #Add finish footer
    content+= str("""\t\t\t\t\t</div>
    \t\t\t\t</div>
    \t\t\t</div>
    \t\t</div>
    \t</div>
    </div>
    """)

print content

placeholder1 = """<div class="col-md-3">"""
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
    
print "END"
