#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re, os, pandas as pd

print("""
     ###########################
     #                         #
     #    SSSSSS               #
     #   SSSSSSSS              #
     #   SS    SS              #
     #   SSS                   #
     #    SSS                  #
     #      SSS                #
     #        SSS              #
     #   SS    SS              #
     #   SSSSSSSS              #
     #    SSSSSS   - CONTENT   #
     #                         #
     ###########################
    """)

print("*** Chris's S content analysis machine v1.1 ***")

filetorun = input("File to run (eg. human): ")

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