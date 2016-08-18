#!/usr/bin/python
from pprint import pprint

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

filters = [
    platforms,
    target,
    developmentLanguage,
    userInterface,
    other,
    license
]

pprint(filters)
print len(filters)

temp = filters[0]
print temp[0]

if "android" in temp:
    print "OK"