![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg) <img alt="GitHub repo size" src="https://img.shields.io/github/repo-size/co2e14/SContent"> <img alt="GitHub top language" src="https://img.shields.io/github/languages/top/co2e14/SContent">

# SContent
Sulphur content analysis of large sequence databases

NB: Required Python3

First go to: ftp://ftp.ebi.ac.uk/pub/databases/fastafiles/uniprotkb to see the list of avaliable databases

To run all in one, run:

```bash
python SulphurContentComplete.py
```

Then enter one of the database names WITHOUT uniprotkb_ infront (eg. pdb or human or rodent).
Should run all the way through.

For some databases, ovevr 16GB RAM is required. (The BIG ones, such as bacteria).

All results are put into a newly created dirrectory data_files.

To run inidividually, the order is:

```bash
python dataprep.py
python S_Percent.py
python SPercentHistogram.py
```

Though only 
```bash
python SPercent Histogram.py
``` 
is needed to redo histogram. Edit this file to change it:

```python
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys

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

print("**** Chris's S content histogram generator v0.5 ****")
print("---- Run after generating files with S_Percent.py ----")
infile = input("Enter table to generate:")
print("Making graph of " + infile + " protein sulphur contents")


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
```

That should be all!
