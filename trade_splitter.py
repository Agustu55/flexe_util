import os.path
import csv
from utilities import create_dir
from utilities import write_out

def split_trades(directory,file,symbols,num_symbols,order_headers):
    order_data = False
    all_orders = {}


    # read file to get assets
    with open(file,mode='r') as csv_file:
        data = csv.reader(csv_file)
        while len(num_symbols) < len(symbols):
            row = next(data)
            if row != ['# orders -- begin'] and row != order_headers:
                try:
                    num_symbols[row[6]] = 'tmp'
                except:
                    print("please enter the symbols in the order they appear in flexemarkets")
                    exit()


    symbol = len(num_symbols) - 1

    # map numbers to symbols
    for key in num_symbols:
        num_symbols[key] = symbols[symbol]
        symbol -= 1


    with open(file,mode='r') as csv_file:
        data = csv.reader(csv_file)
        for row in data:
            if row == ['# orders -- begin']:
                order_data = True
                continue
            if row == ['# orders -- end']:
                order_data = False
                continue

            if order_data and row != order_headers:
                session = row[4]
                market = num_symbols[row[6]]
                order = row[8]
                original = row[9]
                supplier = row[10]
                type = row[12]
                side = row[13]

                # only record limit orders
                if type == 'LIMIT':
                    if order==original and order==supplier:

                        ##make session directory
                        session_dir = directory + os.sep + session
                        create_dir(session_dir)

                        filepath = os.path.join(session_dir + os.sep + market+'-'+side+'.csv')
                        write_out(filepath, row)

                # store all orders by their order id
                all_orders[order]=row

    # re-loop over rows to find trades
    with open(file,mode='r') as csv_file:
        data = csv.reader(csv_file)
        for row in data:
            if row == ['# orders -- begin']:
                order_data = True
                continue
            if row == ['# orders -- end']:
                order_data = False
                continue

            if order_data and row != order_headers:
                session = row[4]
                market = num_symbols[row[6]]
                original = row[9]
                consumer = row[11]
                type = row[12]

                #find limit orders
                if consumer != "NULL" and consumer != "0" and type == "LIMIT":
                    consumer_order = all_orders[consumer]
                    #consumer order has to be limit order
                    if consumer_order[12] == "LIMIT":

                        ##make session directory
                        session_dir = directory + os.sep + session
                        create_dir(session_dir)

                        filepath = os.path.join(session_dir + os.sep + market + '-trades.csv')

                        #find the youngest order for the trades file
                        if (int(original) > int(consumer)):
                            write_out(filepath,row)
                        else:
                            write_out(filepath,consumer_order)

    return num_symbols

