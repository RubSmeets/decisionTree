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

frameworksCopyStage2 = copy.deepcopy(frameworksCopy)

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
        frameworksCopyStage2[i]["thumb_img"] = foundImg
        found = 0
    else:
        frameworksCopyStage2[i]["thumb_img"] = "../img/logos/notfound.png"

# !IMPORTANT change "frameworksCopyStage2" to "frameworksFinal"
# in output write --> to wrap the final json in a data object
# e.g.:
# {
#   "data": {
#       ... 
#   }   
# }
# Insert new element "data"
frameworksFinal = []
for i in range(0, numOfElements):
    frameworksFinal.append({"data":{}});
# format existing key,value to fit into new data object
for i in range(0, numOfElements):
    for key, value in frameworksCopyStage2[i].iteritems():
        frameworksFinal[i]["data"][key] = value

# write output to file
with open('trimmed_frameworks.json', 'w') as data_file:
    print "Write to file trimmed_frameworks.json"
    data_file.write(json.dumps(frameworksCopyStage2, indent=2))

#Move generated file and create backup of original
if os.path.isfile("../../../php/trimmed_frameworks.json"):
    print "file found " + "trimmed_frameworks.json"
    os.rename("../../../php/trimmed_frameworks.json", ("../../../php/trimmed_frameworks_org" + time.strftime("-%d_%m_%y-%H_%M") + ".json"))
    print "Create backup trimmed_frameworks.json"
    os.rename("./trimmed_frameworks.json", "../../../php/trimmed_frameworks.json")
    print "moved new file to php folder"

print "-- FINISHED thumb data generation --"