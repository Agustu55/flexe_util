import sys
import os
import shutil
from collections import OrderedDict

from equilibrium_price import calculate_equilibriums
from graphing_tool import create_graphs
from utilities import create_dir
from trade_splitter import split_trades

headers = ['account', 'email', 'owner', 'marketplace', 'session', 'period', 'market', 'target', 'order',
                 'original', 'supplier', 'consumer', 'type', 'side', 'units', 'price', 'createdDate',
                 'lastModifiedDate', 'clientDescription']
try:
    file = str(sys.argv[1])
    symbols = sys.argv[2:]
except:
    symbols = ['A','B']
    print("unexpected arguement")

num_symbols = OrderedDict()
file = os.path.abspath(file)
name = os.path.basename(file)

print("file name " + name)
print("file path " +file)
print("file dir " + os.path.dirname(file))
directory = os.path.dirname(file) + os.sep + name + '.dir'
print("will make dir here: " + directory)

if os.path.isdir(directory):
    # delete old dir
    shutil.rmtree(directory)
    create_dir(directory)

create_dir(directory)

print("splitting transactions...")
symbol_dict = split_trades(directory,file,symbols,num_symbols,headers)
print("calculating equilibrium...")
rolls = calculate_equilibriums(directory,file,symbols,symbol_dict,headers)
print("creating graphs...")
create_graphs(directory,headers,symbols,rolls)