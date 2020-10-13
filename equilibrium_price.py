## the equilibrium price tool calculates the average equilibrium price at the end of the trading session
## this tool also produces the trading agents which is useful for color coordinated graphing
import csv
import os
import copy

from utilities import write_out


def update_equilibrium(full_assets,row,symbol_dict):
    order_value = symbol_dict[row[6]]+'_' + row[13]
    price = int(row[15])
    side = row[13]
    # update buy prices if the most recent buy is greater
    if side == 'BUY':
        if (int(price) > full_assets[order_value]):
            full_assets[order_value] = (price)
    # update sell prices if the most recent is less than or has not been initialized
    elif side == 'SELL':
        if (full_assets[order_value] == 0 or int(price) < full_assets[order_value]):
            full_assets[order_value] = (int(price))

def calculate_equilibriums(directory,file,letters,symbol_dict,order_headers):
    session = 0;
    sides = ['BUY','SELL']

    # build a new dictionary to store both sides of the assets
    full_assets = {}
    for side in sides:
        for key in symbol_dict:
            asset_side_key = symbol_dict[key] +'_'+ side
            full_assets[asset_side_key] = 0


    session_assets = {}
    session_rolls = {}
    rolls = {}

    equilibrium_prices = []
    order_data = False
    with open (file,newline='') as csvfile:
        data = list(csv.reader(csvfile))
        for row in data:
            if '# orders -- begin' in row:
                order_data = True
                continue

            if '# orders -- end' in row:
                order_data = False
                # copy to full assets to the session
                session_assets[session] = copy.deepcopy(full_assets)
                session_rolls[session] = rolls

                # reset unique session objects
                for key in full_assets:
                    full_assets[key] = 0
                rolls = {}
                equilibrium_prices.append('\n')
                continue

            # get the final prices of the bots with the narrowest spread
            if order_data and row != order_headers:
                session = row[4]
                email = row[1]
                roll = row[18]

                # todo: this will work for robots but what about web. Also how do you account for multiple accounts using different agents.
                # todo: would also be nice to show the risk aversion
                agent = str.rstrip(str.split(roll,'0.3.0')[0],' ')
                # find the location of the first symbol.. that's the start of the paramaters.
                start_param_loc = str.find(roll,str(' ' + letters[0] + ' '))
                paramaters = str.lstrip(roll[start_param_loc:],' ')
                #store the roll for the specefic email
                rolls[email] = agent+' '+paramaters

                # add final outstanding orders (null consumers) to the session prices
                if (row[11] == 'NULL'):
                    equilibrium_prices.append(row)
                    update_equilibrium(full_assets,row,symbol_dict)


    ##write equilibrium price data and trader info to csv file
    filepath = os.path.join(directory + os.sep + 'equilibrium.csv')
    for equilibrium_price in equilibrium_prices:
        write_out(filepath,equilibrium_price)

    for key, value in session_assets.items():
        write_out(filepath, ['Equilibrium Prices'])
        write_out(filepath,[key])
        for innerkey, innervalue in value.items():
            write_out(filepath,[innerkey, innervalue])
        for traderkey, traderroll in session_rolls[key].items():
            write_out(filepath,[traderkey, traderroll])

        write_out(filepath,[''])

    return session_rolls


