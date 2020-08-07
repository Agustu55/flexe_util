import os
import csv

def create_dir(dirpath):
    if not os.path.isdir(dirpath):
        os.mkdir(dirpath)

def write_out(filepath, data):
    # with open(filepath,mode='a',newline='') as file:
    #     writer = csv.writer(file, delimiter=',')
    #     writer.writerow(data)
    pass