#!/usr/bin/python
import json
import os
import time
import sys
import copy

technology = [
    "webtonative",
    "nativejavascript",
    "runtime",
    "javascript_tool",
    "sourcecode",
    "appfactory",
]

platforms = [
    "android",
    "ios",
    "blackberry",
    "windowsphone",
    "wup",
    "androidtv",
    "appletv",
    "watchos",
    "bada",
    "firefoxos",
    "kindle",
    "webos",
    "osx",
    "windows",
    "windowsmobile",
    "symbian",
    "tizen",
    "maemo",
    "meego"
]

languages = [
    "html",
    "csharp",
    "css",
    "basic",
    "cplusplus",
    "java",
    "javame",
    "js",
    "jsx",
    "lua",
    "objc",
    "swift",
    "php",
    "python",
    "ruby",
    "actionscript",
    "MXML",
    "visualeditor",
    "xml",
    "qml"
]

outputType = [
    "mobilewebsite",
    "webapp",
    "nativeapp",
    "hybridapp"
]

cost = [
    "free",
    "trial"
]

frameworkHeaderCallOrder = [
    # framework props
    "framework"
]

toolSpecificationCallOrder = [
    technology,
    "announced",
    "framework_current_version",
    platforms,
    languages,
    outputType,
    "license",
    "opensource",
    cost
]

developmentSpecificationCallOrder = [
    "games",
    "clouddev",
    "allows_prototyping",
    "multi_screen",
    "livesync",
    "publ-assist"
]

hardwareFeaturesCallOrder = [
    "accelerometer",
    "device",
    "file",
    "bluetooth",
    "camera",
    "capture",
    "compass",
    "connection",
    "contacts",
    "geolocation",
    "gestures_multitouch",
    "nativeevents",
    "nfc",
    "storage",
    "messages_telephone",
    "vibration"    
]

supportFeaturesCallOrder = [
    "onsite_supp",
    "hired_help",
    "phone_supp",
    "time_delayed_supp",
    "community_supp"  
]

formatKey = {
    "true": """<i class="glyphicon glyphicon-ok check"></i>""",
    "false": """<i class="glyphicon glyphicon-remove uncheck"></i>""",
    "UNDEF": """<i class="glyphicon glyphicon-minus"></i>""",
    "EMPTY": """<i class="glyphicon glyphicon-minus"></i>""",
    "none": """<i class="glyphicon glyphicon-minus"></i>""",
    "via": """<i class="fa fa-plug"></i>""",
    "partially": "Partially",
    "soon": "Soon",

    "active":"Active",
    "discontinued":"Discontinued",

    "trial": "Trial version",

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

# Format the name to lowercase and without special characters
def formatString( str ):
    output = str.replace('/','').replace(' ', '').replace('-','').replace('.','')
    return output.lower()

print "-- START comparison data generation --"

# Read the contents of the existing json file
print "Read frameworks json..."
with open('frameworks.json', 'r') as data_file:
    frameworks = json.load(data_file)
numOfElements = len(frameworks)

# Create list with imageNames from existing logos in folder "../img/logos/"
imgList = []
for path, dirs, files in os.walk("../../../img/logos"):
  for f in files:
    f = "../img/logos/" + f
    imgList.append(f)

# Insert new element "header"
jsonData = []
for i in range(0, numOfElements):
    jsonData.append({"header":""});

def createToolSpecification():
    contentsToolSpecification = ""
    for i in range(0, numOfElements):
        contentsToolSpecification = ""
        for idx, item in enumerate(toolSpecificationCallOrder):
            if(isinstance(item, basestring)):
                for key, value in frameworks[i].iteritems():
                    if(key == item) and item == "opensource" and value and value != "none" and value != "UNDEF" and value != "EMPTY":
                        contentsToolSpecification += str("""<div class="feature-item"><span>""" + str(formatKey.get(value)) + """</span></div>""")
                    elif(key == item) and value and value != "none" and value != "UNDEF" and value != "EMPTY":
                        contentsToolSpecification += str("""<div class="feature-item"><span>""" + str(value) + """</span></div>""")
            else:
                #we have a list
                contentsToolSpecification += str("""<div class="feature-item">""")
                for nestedItem in item:
                    for key, value in frameworks[i].iteritems():
                        if (nestedItem == key):
                            #technology
                            if value != "none" and value != "UNDEF" and value != "EMPTY" and value != "false":
                                contentsToolSpecification += str("""<span>""" + str(formatKey.get(key)) + """</span>""") 
                contentsToolSpecification += str("""</div>""")
        jsonData[i]["tool_specification"] = contentsToolSpecification

def createDevelopmentSpecification():
    contentsDevSpec = ""
    for i in range(0, numOfElements):
        contentsDevSpec = ""
        for idx, item in enumerate(developmentSpecificationCallOrder):
            for key, value in frameworks[i].iteritems():
                if(key == item) and value:
                    contentsDevSpec += str("""<div class="feature-item"><span>""" + str(formatKey.get(value)) + """</span></div>""")
        jsonData[i]["dev_specification"] = contentsDevSpec

def createHardwareFeatures():
    contentsHardwareFeat = ""
    for i in range(0, numOfElements):
        contentsHardwareFeat = ""
        for idx, item in enumerate(hardwareFeaturesCallOrder):
            for key, value in frameworks[i].iteritems():
                if(key == item) and value:
                    contentsHardwareFeat += str("""<div class="feature-item"><span>""" + str(formatKey.get(value)) + """</span></div>""")
        jsonData[i]["hardware_features"] = contentsHardwareFeat

def createSupportFeatures():
    contentsSupportFeat = ""
    for i in range(0, numOfElements):
        contentsSupportFeat = ""
        for idx, item in enumerate(supportFeaturesCallOrder):
            for key, value in frameworks[i].iteritems():
                if(key == item) and value:
                    contentsSupportFeat += str("""<div class="feature-item"><span>""" + str(formatKey.get(value)) + """</span></div>""")
        jsonData[i]["support_features"] = contentsSupportFeat


contentsHeader = ""
foundImg = ""
for i in range(0, numOfElements):
    foundImg = ""
    contentsHeader = ""
    for key, value in frameworks[i].iteritems():
        #Create the header markup
        for idx, item in enumerate(frameworkHeaderCallOrder):
            if item == key:
                contentsHeader = """<div class="framework-header">"""
                for img in imgList:
                    if(formatString(value) in img):
                        foundImg = img
                if foundImg != "":
                    contentsHeader += """<img src=\"""" + str(foundImg) + """\" alt="">"""
                else:
                    contentsHeader += """<img src="../img/logos/notfound.png" alt="">"""
                contentsHeader += """<table class="caption"><tr><td style="width:40px"><span class="glyphicon glyphicon-remove-circle"></span></td><td align="left"><h4 class="thumb-caption">""" + str(value) + """</h4></td></tr></table></div>"""
                jsonData[i]["header"] = contentsHeader
                jsonData[i]["framework"] = value

#Create the tool specifications markup
createToolSpecification() 

#Create the development specifications markup
createDevelopmentSpecification()

#Create the hardware features markup
createHardwareFeatures()

#Create the support features markup
createSupportFeatures()

# write output to file
with open('framework_compare.json', 'w') as data_file:
    print "Write to file framework_compare.json"
    data_file.write(json.dumps(jsonData, indent=2))

print "-- FINISHED comparison data generation --"