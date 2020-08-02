import pandas as pd
import os.path
from pathlib import Path
import matplotlib.pyplot as plt
import argparse
import sys
import csv



def create_dir(dirpath):
    if not os.path.isdir(dirpath):
        os.mkdir(dirpath)

print("hello, world")
file = ""
try:
    file = str(sys.argv[1])
except:
    # todo: not allowed in production
    file = "../Transaction Data/modify.csv"
    print("unexpected arguement")

all_orders = {}
print(file)
name = file.split('/')[-1]
print(name)
file = os.path.abspath(file)
directory = os.path.dirname(file) + os.sep + name + '.dir'
create_dir(directory)
print(directory)
order_headers = ['account', 'email', 'owner', 'marketplace', 'session', 'period', 'market', 'target', 'order', 'original', 'supplier', 'consumer', 'type', 'side', 'units', 'price', 'createdDate', 'lastModifiedDate', 'clientDescription']
holding_headers = 0
order_data = False

def write_out(filepath, data):
    with open(filepath,mode='a',newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(data)


with open(file,mode='r') as csv_file:
    data = csv.reader(csv_file)
    data_2 = csv.reader(csv_file)
    for row in data:
        if row == ['# orders -- begin']:
            print('orders starting')
            order_data = True
            continue
        if row == ['# orders -- end']:
            print('orders ended')
            order_data = False
            continue

        if order_data and row != order_headers:
            marketplace = row[3]
            session = row[4]
            market = row[6]
            order = row[8]
            original = row[9]
            supplier = row[10]
            consumer = row[11]
            type = row[12]
            side = row[13]

            # only record limit orders
            if type == 'LIMIT':
                if order==original and order==supplier:
                    ## make marketplace directory
                    marketplace_dir = directory + os.sep + marketplace
                    create_dir(marketplace_dir)

                    ##make session directory
                    session_dir = marketplace_dir + os.sep + session
                    create_dir(session_dir)

                    filepath = os.path.join(session_dir + os.sep + market+'-'+side+'.csv')
                    write_out(filepath, row)

            # store all orders by their order id
            all_orders[order]=row
    print(all_orders)

# re-loop over rows to find trades
with open(file,mode='r') as csv_file:
    data = csv.reader(csv_file)
    for row in data:
        if row == ['# orders -- begin']:
            print('orders starting')
            order_data = True
            continue
        if row == ['# orders -- end']:
            print('orders ended')
            order_data = False
            continue

        if order_data and row != order_headers:
            marketplace = row[3]
            session = row[4]
            market = row[6]
            order = row[8]
            original = row[9]
            supplier = row[10]
            consumer = row[11]
            type = row[12]
            side = row[13]

            #find limit orders
            if consumer != "NULL" and consumer != "0" and type == "LIMIT":
                consumer_order = all_orders[consumer]
                #consumer order has to be limit order
                if consumer_order[12] == "LIMIT":

                    ## make marketplace directory
                    marketplace_dir = directory + os.sep + marketplace
                    create_dir(marketplace_dir)

                    ##make session directory
                    session_dir = marketplace_dir + os.sep + session
                    create_dir(session_dir)

                    filepath = os.path.join(session_dir + os.sep + market + '-trades.csv')

                    #find the youngest order for the trades file
                    if (int(original) > int(consumer)):
                        write_out(filepath,row)
                    else:
                        write_out(filepath,consumer_order)

