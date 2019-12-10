#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request as request
from contextlib import closing
import shutil as sh
import gzip, os

#import ftplib
#from datetime import datetime
# WORKING ON LISTING AVALIABLE FILES
#now = datetime.now()
#print("Current list of uniprotkb datafiles from ", now)

print("Creating data files directory")
dirName = "data_files"
if not os.path.exists(dirName):
    os.mkdir(dirName)
    print("Directory ", dirName, " created")
else:
    print("Directory", dirName, "already exists")

todl = input("File to download (eg. human): ")
inFile = "data_files/uniprotkb_" + todl + ".gz"
outFile = "data_files/uniprotkb_" + todl
filetodl = "ftp://ftp.ebi.ac.uk/pub/databases/fastafiles/uniprotkb/uniprotkb_" + todl + ".gz"

print("Downloading " + todl + " sequences file from: " + filetodl)

with closing(request.urlopen(filetodl)) as r:
    with open("data_files/uniprotkb_" + todl + ".gz", "wb") as f:
        sh.copyfileobj(r, f)

print("Finished downloading " + todl + " sequences")

size = os.stat(f'{inFile}').st_size
print(f"size of {inFile} = {size/1024**3:.2f} GB")

print("Unzipping " + todl + " sequences")

with gzip.open("data_files/uniprotkb_" + todl + ".gz", "rb") as f_in:
    with open("data_files/uniprotkb_" + todl, "wb") as f_out:
        sh.copyfileobj(f_in, f_out)
        
size = os.stat(f'{outFile}').st_size
print(f"size of {outFile} = {size/1024**3:.2f} GB")
print("Cleaning up...")

os.remove("data_files/uniprotkb_" + todl + ".gz")      
        
print("*** Finished with " + todl + " sequence file, ready to run S_Percent.py ***")