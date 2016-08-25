#!/usr/bin/python
import json
import os
from shutil import copyfile
import os.path
import time

if os.path.isfile("../index.html"):
    print "file found " + "index.html"
    os.rename("../index.html", ("../index_org" + time.strftime("-%d_%m_%y-%H_%M") + ".html"))
    os.rename("./index.html", "../index.html")
