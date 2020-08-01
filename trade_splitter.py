import pandas as pd
import os.path
from pathlib import Path
import matplotlib.pyplot as plt
import argparse
import sys
import csv

print("hello, world")
file = ""
try:
    file = str(sys.argv[1])
except:
    # todo: not allowed in production
    file = "../Transaction Data/modify.csv"
    print("unexpected arguement")

print(file)
name = file.split('/')[-1]
print(name)
file = os.path.abspath(file)
print(file)

with open(file,mode='r') as csv_file:
    data = csv.reader(csv_file)
    for row in data:
        if '# orders -- begin' in row:
            print("start of trades")
            print(next(data));
        if '# orders -- end' in row:
            print("end of trades")
        if '# holdings -- begin' in row:
            print("start of holdings")
            print(next(data))
        if '# holdings -- end' in row:
            print("end of holdings")





