#!/usr/bin/python
import json
import os
import time
import sys

frameworkKeyCallOrder = [
    # framework props
    "comparison_data_last_update",
    "framework",
    "framework_current_version",
    "announced",
    "market",
    "twitter",
    "stackoverflow",
    "appshowcase",
    "clouddev",
    "license",
    "learning_curve",
    "allows_prototyping",
    "perf_overhead",
    "integrate_with_existing_app",
    "iteration_speed",
    "remoteupdate",
    "free",
    "opensource",
    "repo",
    "trial",
    "games",
    "multi_screen",
    # Support 
    "onsite_supp",
    "hired_help",
    "phone_supp",
    "time_delayed_supp",
    "community_supp",
    # Development
    "publ-assist",
    "livesync",
    "code_sharing",
    # resources
    "documentation_url",
    "book",
    "video_url",
    "tutorial_url",
    "url",
    #technology
    "webtonative",
    "nativejavascript",
    "runtime",
    "javascript_tool",
    "sourcecode",
    "appfactory",
    #output product
    "mobilewebsite",
    "webapp",
    "nativeapp",
    "hybridapp",
    #supported platforms
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
    "meego",
    #programming languages
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
    "qml",
    #additional features
    "ads",
    "cd",
    "encryption",
    "sdk",
    "widgets",
    "animations",
    #supported device features
    "accelerometer",
    "device",
    "file",
    "bluetooth",
    "camera",
    "capture",
    "geolocation",
    "gestures_multitouch",
    "compass",
    "connection",
    "contacts",
    "messages_telephone",
    "nativeevents",
    "nfc",
    "notification",
    "accessibility",
    "status",
    "storage",
    "vibration"
]


print "-- START FRAMEWORK CMS --"

# Read the contents of the existing json file
print "Read frameworks..."
with open('frameworks.json', 'r') as data_file:
    frameworks = json.load(data_file)

def editFramework ( framework ):
    for idx, item in enumerate(frameworkKeyCallOrder):
        for key, value in framework.iteritems():
            if item == key:
                if item == "comparison_data_last_update":
                    framework[key] = time.strftime("%d.%m.%y")
                elif item == "framework_current_version":
                    input = raw_input('Enter value for ' + key + ' (default=' + value + ') (DEFAULT/abc..): ')
                    if(input == ""):
                        framework[key] = value
                    else:
                        framework[key] = input
                elif(value == "UNDEF" or value == "EMPTY"):
                    if(idx < frameworkKeyCallOrder.index("accelerometer")):#starting from features the default empty is "EMPTY"
                        input = raw_input('Enter value for ' + key + ' (y/N/s/p/v/""/abc..): ')
                        if(input == ""):
                            framework[key] = "false"
                        elif(input == "y"):
                            framework[key] = "true"
                        elif(input == "n"):
                            framework[key] = "false"
                        elif(input == "s"):
                            framework[key] = "soon"
                        elif(input == "v"):
                            framework[key] = "via"
                        elif(input == "p"):
                            framework[key] = "partially"
                        else:
                            framework[key] = input
                    else:
                        input = raw_input('Enter value for ' + key + ' (y/n/s/p/v/""/abc..): ')
                        if(input == ""):
                            framework[key] = "EMPTY"
                        elif(input == "y"):
                            framework[key] = "true"
                        elif(input == "n"):
                            framework[key] = "false"
                        elif(input == "s"):
                            framework[key] = "soon"
                        elif(input == "v"):
                            framework[key] = "via"
                        elif(input == "p"):
                            framework[key] = "partially"
                        else:
                            framework[key] = input
                elif(value == "soon"):
                    input = raw_input('Enter value for ' + key + ' (y/n/S/p/v/""/abc..): ')
                    if(input == ""):
                        framework[key] = "soon"
                    elif(input == "y"):
                        framework[key] = "true"
                    elif(input == "n"):
                        framework[key] = "false"
                    elif(input == "s"):
                        framework[key] = "soon"
                    elif(input == "v"):
                        framework[key] = "via"
                    elif(input == "p"):
                        framework[key] = "partially"
                    else:
                        framework[key] = input
    print "Updated framework: "
    for key, value in framework.iteritems():
        print "\t" + key + " :" + value 


newFramework = frameworks[0].fromkeys(frameworks[0], "EMPTY")
#print "orginal"
#for key, value in frameworks[0].iteritems():
#    print key + "->" + value

#print "\nnew"
#for key, value in newFramework.iteritems():
#    print key + "->" + value

# Start reading user input
print "-------------------------"
print "\n"
numOfFrameworks = len(frameworks)
input = ""
frameworkIndex = -1
changed = 0
frameworkName = ""

while (input == ""):
    frameworkIndex = -1
    input = raw_input('Enter framework name (\"q\" to quit): ')

    if input.lower() == "q":
        if changed == 1:
            input = raw_input('Save changes (y/N)?: ')
            if input == "y":
                with open('frameworks.json', 'w') as data_file:
                    data_file.write(json.dumps(frameworks, indent=2, sort_keys=True))
                    print "Changes saved!"
            
        print "Exiting program"
        sys.exit()
    
    frameworkName = input
    for i in range(0, numOfFrameworks):
        for key, value in frameworks[i].iteritems():
            if frameworkName.lower() == value.lower():
                frameworkIndex = i
                print "Framework found: " + value
    
    if frameworkIndex != -1:
        input = raw_input('Want to edit ' + frameworkName + '? (y/N): ')
        if (input == "y"):
            editFramework(frameworks[frameworkIndex])
            changed = 1
    else:
        input = raw_input('Would you like to add new framework: ' + input + ' (y/N)? ')
        if input == "y":
            print "Creating new framework with name " + frameworkName
            newFramework["framework"] = frameworkName
            editFramework(newFramework)
            frameworks.append(newFramework)
            changed = 1
    
    input = ""
