#!/usr/bin/python
import json
import os
import time
import sys
import copy

frameworkHeaderCallOrder = [
    # framework props
    "framework"
]

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

# Insert new element "data"
jsonData = []
for i in range(0, numOfElements):
    jsonData.append({"header":""});


contents = ""
foundImg = ""
for i in range(0, numOfElements):
    foundImg = ""
    for key, value in frameworks[i].iteritems():
        for idx, item in enumerate(frameworkHeaderCallOrder):
            if item == key:
                contents = """<div class="framework-header">"""
                for img in imgList:
                    if(formatString(value) in img):
                        foundImg = img
                if foundImg != "":
                    contents += """<img src=\"""" + str(foundImg) + """\" alt="">"""
                contents += """<table class="caption"><tr><td style="width:40px"><span class="glyphicon glyphicon-remove-circle"></span></td><td align="left"><h4 class="thumb-caption">""" + str(value) + """</h4></td></tr></table></div>"""
                jsonData[i]["header"] = contents
                jsonData[i]["framework"] = value

# write output to file
with open('framework_compare.json', 'w') as data_file:
    print "Write to file framework_compare.json"
    data_file.write(json.dumps(jsonData, indent=2))

print "-- FINISHED comparison data generation --"