#!/usr/bin/python
import json
import os
import time
import sys
import copy

frameworkKeyCallOrder = [
    # framework props
    "framework",
    "status"
]

# Format the name to lowercase and without special characters
def formatString( str ):
    output = str.replace('/','').replace(' ', '').replace('-','').replace('.','')
    return output.lower()

print "-- START thumb data generation --"

# Read the contents of the existing json file
print "Read frameworks json..."
with open('frameworks.json', 'r') as data_file:
    frameworks = json.load(data_file)

# Create deepcopy of dictionary for modification purposes
frameworksCopy = copy.deepcopy(frameworks)


numOfElements = len(frameworks)
found = 0;

for i in range(0, numOfElements):
    for key, value in frameworks[i].iteritems():
        for idx, item in enumerate(frameworkKeyCallOrder):
            if item == key:
                found = 1
        if(found == 0):
            del frameworksCopy[i][key]
        found = 0

frameworksFinalCopy = copy.deepcopy(frameworksCopy)

# Create list with imageNames from existing logos in folder "../img/logos/"
imgList = []
for path, dirs, files in os.walk("../../../img/logos"):
  for f in files:
    f = "../img/logos/" + f
    imgList.append(f)  #strip ".png" from logo names  

found = 0
foundImg = ""
for i in range(0, numOfElements):
    for key, value in frameworksCopy[i].iteritems():
        for img in imgList:
            if(formatString(value) in img):
                foundImg = img
                found = 1
    if(found == 1):
        frameworksFinalCopy[i]["thumb_img"] = foundImg
        found = 0
    else:
        frameworksFinalCopy[i]["thumb_img"] = "../img/logos/notfound.png"

with open('trimmed_frameworks.json', 'w') as data_file:
    print "Write to file trimmed_frameworks.json"
    data_file.write(json.dumps(frameworksFinalCopy, indent=2))

print "-- FINISHED thumb data generation --"