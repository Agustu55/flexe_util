import sys
import os
from collections import OrderedDict

from equilibrium_price import calculate_equilibriums
from utilities import create_dir
from trade_splitter import split_trades

headers = ['account', 'email', 'owner', 'marketplace', 'session', 'period', 'market', 'target', 'order',
                 'original', 'supplier', 'consumer', 'type', 'side', 'units', 'price', 'createdDate',
                 'lastModifiedDate', 'clientDescription']
try:
    file = str(sys.argv[1])
    letters = sys.argv[2:]
except:
    # todo: not allowed in production
    file = "../Transaction Data/modify.csv"
    letters = ['A','B']
    print("unexpected arguement")

symbols = OrderedDict()
print(file)
name = file.split('/')[-1]
print(name)
file = os.path.abspath(file)
directory = os.path.dirname(file) + os.sep + name + '.dir'
create_dir(directory)
print(directory)

print("calling trade_splitter from controller")
symbol_dict = split_trades(directory,file,letters,symbols,headers)
print("calling calculate equilibrium from controller")
calculate_equilibriums(directory,file,letters,symbol_dict,headers)

