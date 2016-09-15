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
    "url",
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

toolSpecificationHeaderCallOrder = [
    "toolTecCon",
    "toolAnnCon",
    "toolVerCon",
    "toolPlaCon",
    "toolLanCon",
    "toolProCon",
    "toolLicCon",
    "toolSrcCon",
    "toolCostCon",
]

developmentSpecificationCallOrder = [
    "games",
    "clouddev",
    "allows_prototyping",
    "multi_screen",
    "livesync",
    "publ_assist"
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

resourcesCallOrder = [
    "url",
    "documentation_url",
    "tutorial_url",
    "video_url",
    "book",
    "appshowcase",
    "market",
    "repo"
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

    "freel": "Proprietary free license",
    "comml": "Proprietary commercial license",
    "enterprisel": "Proprietary enterprise license",
    "trial": "Trial version",

    "nativejavascript": "Native JS",
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

    "url": "Homepage",
    "documentation_url": "Official Docs",
    "tutorial_url": "Tutorial",
    "video_url": "Video Introduction",
    "book": "Recommended Book",
    "appshowcase": "App Gallery",
    "market": "Market",
    "repo": "Repository",
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
    licenseName = ""
    for i in range(0, numOfElements):
        for idx, item in enumerate(toolSpecificationCallOrder):
            contentsToolSpecification = ""
            if(isinstance(item, basestring)):
                for key, value in frameworks[i].iteritems():
                    if (key == item) and key == "license" and value and value != "none" and value != "UNDEF" and value != "EMPTY":
                        if "|" in value:
                            contentsToolSpecification += str("""<ul class="feature-item">""")
                            licenses = value.split("|")
                            for license in licenses:
                                if "free" in license:
                                    licenseName = formatKey.get("freel");
                                elif "commercial" in license:
                                    licenseName = formatKey.get("comml");
                                elif "enterprise" in license:
                                    licenseName = formatKey.get("enterprisel");
                                else:
                                    licenseName = license
                                contentsToolSpecification += str("""<li>""" + str(licenseName) + """</li>""")
                            contentsToolSpecification += str("""</ul>""")
                        else:
                            if "free" in value:
                                licenseName = formatKey.get("freel");
                            elif "commercial" in value:
                                licenseName = formatKey.get("comml");
                            elif "enterprise" in value:
                                licenseName = formatKey.get("enterprisel");
                            else:
                                licenseName = value
                            contentsToolSpecification += str("""<div class="feature-item"><span>""" + str(licenseName) + """</span></div>""")
                    elif(key == item) and item == "opensource" and value and value != "none" and value != "UNDEF" and value != "EMPTY":
                        contentsToolSpecification += str("""<div class="feature-item"><span>""" + str(formatKey.get(value)) + """</span></div>""")
                    elif(key == item) and value and value != "none" and value != "UNDEF" and value != "EMPTY":
                        contentsToolSpecification += str("""<div class="feature-item"><span>""" + str(value) + """</span></div>""")
                    elif(key == item) and value:
                        contentsToolSpecification += str("""<div class="feature-item"><span>""" + str(formatKey.get(value)) + """</span></div>""")
                jsonData[i][toolSpecificationHeaderCallOrder[idx]] = contentsToolSpecification
            else:
                #we have a list
                if idx == 5: #for output Type
                    contentsToolSpecification += str("""<ul class="feature-item">""")
                    for nestedItem in item:
                        for key, value in frameworks[i].iteritems():
                            if (nestedItem == key):
                                if value != "none" and value != "UNDEF" and value != "EMPTY" and value != "false":
                                    contentsToolSpecification += str("""<li>""" + str(formatKey.get(key)) + """</li>""")
                    contentsToolSpecification += str("""</ul>""")
                else:
                    contentsToolSpecification += str("""<div class="feature-item">""")
                    for nestedItem in item:
                        for key, value in frameworks[i].iteritems():
                            if (nestedItem == key):
                                if value != "none" and value != "UNDEF" and value != "EMPTY" and value != "false":
                                    contentsToolSpecification += str("""<span>""" + str(formatKey.get(key)) + """</span>, """) 
                    contentsToolSpecification = contentsToolSpecification[:-2]  #remove last ", " from string
                    contentsToolSpecification += str("""</div>""")
                jsonData[i][toolSpecificationHeaderCallOrder[idx]] = contentsToolSpecification

def createDevelopmentSpecification():
    contentsDevSpec = ""
    for i in range(0, numOfElements):
        contentsDevSpec = ""
        for idx, item in enumerate(developmentSpecificationCallOrder):
            for key, value in frameworks[i].iteritems():
                if(key == item) and value:
                    if value == "via":
                        contentsDevSpec += str("""<div class="feature-item"><span><i class="fa fa-users"></i></span></div>""")
                    else:
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

def createResources():
    contentsResources = ""
    for i in range(0, numOfElements):
        contentsResources = ""
        for idx, item in enumerate(resourcesCallOrder):
            for key, value in frameworks[i].iteritems():
                if(key == item):
                    if value == "UNDEF" or value == "EMPTY" or value == "none":
                        contentsResources += str("""<div class="feature-item"><span>""" + str(formatKey.get(value)) + """</span></div>""")
                    elif value == "false":
                        contentsResources += str("""<div class="feature-item"><span>""" + str(formatKey.get("EMPTY")) + """</span></div>""")
                    else:
                        if key == "book":
                            if "http" not in value:
                                contentsResources += str("""<div class="feature-item"><span>""" + str(value) + """</span></div>""")
                            else:
                                contentsResources += str("""<div class="feature-item"><a href=\"""" + value + """\" target="_blank">""" + str(formatKey.get(key)) + """</a></div>""")
                        elif "|" in value:
                            contentsResources += str("""<div class="feature-item">""")
                            nestedValues = value.split("|")
                            contentsResources += str("""<a href=\"""" + nestedValues[0] + """\" target="_blank">""" + str(formatKey.get(key)) + """(1)</a>, """)
                            for idx2, nestedItem in enumerate(nestedValues):
                                if idx2 != 0:
                                    contentsResources += str("""<a href=\"""" + nestedItem + """\" target="_blank">(""" + str(idx2+1) + """)</a>, """)
                            contentsResources = contentsResources[:-2]  #remove last ", " from string
                            contentsResources += str("""</div>""")
                        else:
                            contentsResources += str("""<div class="feature-item"><a href=\"""" + value + """\" target="_blank">""" + str(formatKey.get(key)) + """</a></div>""")
        jsonData[i]["resources"] = contentsResources


contentsHeader = ""
foundImg = ""
for i in range(0, numOfElements):
    foundImg = ""
    contentsHeader = ""
    urls = ["#"]
    lastUpdate = frameworks[i].get("comparison_data_last_update")
    for idx, item in enumerate(frameworkHeaderCallOrder):
        for key, value in frameworks[i].iteritems():
            #Create the header markup
            if item == key:
                if key == "url":
                    if "|" in value:
                        urls = value.split("|")
                    elif value == "UNDEF" or value == "EMPTY" or value == "none" or value == "false":
                        urls[0] = "#"
                    else:
                        urls[0] = value
                else:
                    contentsHeader = """<div class="framework-header"><table class="caption"><colgroup><col style="width:40px" /><col style="width:140px" /></colgroup>"""
                    for img in imgList:
                        if(formatString(value) in img):
                            foundImg = img
                    if foundImg != "" and urls[0] != "#":
                        contentsHeader += """<tr><td colspan="2"><a href=\"""" + str(urls[0]) + """\" target="_blank"><img src=\"""" + str(foundImg) + """\" alt=""></a></td></tr>"""
                    elif urls[0] != "#":
                        contentsHeader += """<tr><td colspan="2"><a href=\"""" + str(urls[0]) + """\" target="_blank"><img src="../img/logos/notfound.png" alt=""></a></td></tr>"""
                    else:
                        contentsHeader += """<tr><td colspan="2"><img src="../img/logos/notfound.png" alt=""></td></tr>"""
                    contentsHeader += """<tr><td width="40"><span class="glyphicon glyphicon-remove-circle"></span></td><td align="left" height="58"><h4 class="thumb-caption">""" + str(value) + """</h4></td></tr>"""
                    contentsHeader += """<tr><td colspan="2" class="data-status">Info updated: """ + lastUpdate + """</td></tr></table></div>"""
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

#Create the resources markup
createResources()

with open('framework_compare.json', 'w') as data_file:
    print "Write to file framework_compare.json"
    data_file.write(json.dumps(jsonData, indent=2))

#Move generated file and create backup of original
if os.path.isfile("../../../php/framework_compare.json"):
    print "file found " + "framework_compare.json"
    os.rename("../../../php/framework_compare.json", ("../../../php/framework_compare_org" + time.strftime("-%d_%m_%y-%H_%M") + ".json"))
    print "Create backup framework_compare.json"
    os.rename("./framework_compare.json", "../../../php/framework_compare.json")
    print "moved new file"

print "-- FINISHED comparison data generation --"