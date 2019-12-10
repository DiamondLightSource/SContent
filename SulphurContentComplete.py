#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request as request
from contextlib import closing
import shutil as sh
import gzip, os, re
import pandas as pd
import sys
import matplotlib.pyplot as plt
import numpy as np

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

filetorun = todl

inFile = "data_files/uniprotkb_" + filetorun
#inFile = "data-files/uniprotkb_human"
outFile = "data_files/results_" + filetorun
size = os.stat(f'{inFile}').st_size
print(f"size of {inFile} = {size/1024**3:.2f} GB")

pattern = r"[>][A-Z]{2}[:]"
pattern = re.compile(pattern)

count = 0
sequence = ""
results = ["length, M, C\n"]

with open(f'{inFile}', 'r') as f:
    for line in f:
        match = pattern.match(line)
        if match:
            if len(sequence):
                results.append(f"{len(sequence)}, {sequence.count('M')}, {sequence.count('C')}\n")
                count += 1
                if count % (1000*1000) == 0: print(count)
                sequence = ""
        else:
            sequence += line

# write out results
with open(f'{outFile}', 'w') as f:
    f.writelines(results)

df = pd.read_csv(f"{outFile}")
print(df)

print("*** Finished parsing " + filetorun + " sequences ***")

infile = todl


def main():
    orig_stdout = sys.stdout
    sys.stdout = open("data_files/stats_" + infile + ".txt", "a")
    print(pd._version)
    column_names = ['length', 'M', 'C']
    sContent = pd.read_csv("data_files/results_" + infile,
                           skiprows = 1,
                           engine = 'python',
                           names = column_names,
                           sep = '[, ]+')
    print(sContent)
    
    C = sContent[['C']]
    M = sContent[['M']]
    L = sContent[['length']]
    sRes = np.add(C, M)
    sDiv = np.divide(sRes, L)
    sPerc = sDiv*100
    
    print(sPerc)
    
    sPerc.hist(bins=500, grid=False, xlabelsize=12, ylabelsize=12)
    plt.title("% sulphur content of proteins - " + infile)
    plt.xlabel("% S", fontsize=15)
    plt.ylabel("Frequency", fontsize=15)
    plt.xlim([0.0, 25])
    plt.savefig("data_files/" + infile + ".png", format='png', bbox_inches='tight', dpi=1000,
                alpha=0.5)
    plt.show()
    
# statistics
    print('Minimum:')
    mini = np.amin(sPerc)
    print(mini)
    print('Maximum:')
    maxi = np.amax(sPerc)
    print(maxi)
    print('Mean:')
    mean = np.mean(sPerc)
    print(mean)
    #print('Harmonic mean:')
    #har_mean = st.harmonic_mean(sPerc)
    #print(har_mean)
    print('Median:')
    median = np.median(sPerc)
    print(median)
    print('Standard Deviation:')
    std = np.std(sPerc)
    print(std)
    print('\n')
    
    sys.stdout.close()
    sys.stdout=orig_stdout

main()

print("Finished")