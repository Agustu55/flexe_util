## graphing tool uses seaborn and trader information to produce trading graphs
from datetime import datetime, timedelta
import pandas as pd
import os.path
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt2
import seaborn as sns
import matplotlib.dates as mdates
from matplotlib import ticker
import time

sns.set(style='ticks')


def create_graphs(directory,headers,symbols,rolls):
    min = datetime.now()
    max = datetime(1900, 1, 1)

    assets = {}
    types = ['BUY', 'SELL', 'trades']
    for symbol in symbols:
        assets[symbol] = types


    # walk the directory to dive into all of the session csvss
    for subdir, dirs, files in os.walk(directory):
        for session in dirs:
            session_directory = subdir + os.sep + session + os.sep
            main_fig, axis = plt.subplots(2, figsize=(20, 8), sharex=True)
            subplot = 0

            # walk through the assets in the session and the BUY SELL trade csvs
            for asset in assets:
                for order_type in assets[asset]:
                    csv_file = session_directory + asset + '-' + order_type + '.csv'

                    # create the dataframe from the trade csv
                    df = pd.read_csv(csv_file, names=headers)

                    # capitalize price and scale by 1000
                    df['Price'] = df['price'] / 100

                    # create a time column from the last modified date and get just the time
                    df['Time'] = df['lastModifiedDate']
                    df['Time'] = df['Time'].str[11:]
                    df['Time'] = pd.to_datetime(df['Time'])

                    # get minimum date for the x limit
                    min = df['Time'].min()
                    max = df['Time'].max()

                    # create a type column for agents based on email
                    df['Type'] = df['email']


                    # update Type to be the robot agent based on the users email in that session
                    df['Type'].replace(rolls[session], inplace=True)

                    # plot differently based on order type
                    if order_type == "BUY":
                        blues = sns.color_palette("GnBu", 10)
                        sns.set_palette(blues)
                        sns.scatterplot(x='Time', y='Price', data=df, hue='Type', legend='brief' if subplot == 0 else "", ax=axis[subplot])
                        pass
                    elif order_type == "SELL":
                        reds = sns.color_palette("Reds", 10)
                        sns.set_palette(reds)
                        sns.scatterplot(x='Time', y='Price', data=df, hue='Type', legend='brief' if subplot == 0 else "", ax=axis[subplot])
                        pass
                    elif order_type == "trades":
                        axis[subplot].plot(df['Time'], df['Price'], color='k', linestyle='None', marker='x', alpha=0.5)

                    sns.despine()
                    axis[subplot].set_title(asset)
                    axis[subplot].xaxis.set_major_locator(plt.MaxNLocator(10));

                    axis[subplot].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
                    axis[subplot].yaxis.set_major_formatter(ticker.FormatStrFormatter('$%1.2f'))
                    axis[subplot].legend().set_visible(False)

                    if subplot == 0:
                        ## draw the legend in a seperate file
                        handles, labels = axis[subplot].get_legend_handles_labels()
                        legend_fig = plt.figure(figsize=(15, 15))
                        legend_fig.legend(handles, labels, loc='center')
                        plt.savefig(directory + os.sep + session + 'legend.png')

                subplot += 1
            plt.gcf().autofmt_xdate()

            ## add (max) and subtract (min) seconds to add white space buffer on plot
            min = min - timedelta(0, 15)
            max = max + timedelta(0, 30)
            min = min.to_pydatetime()
            max = max.to_pydatetime()

            plt.suptitle('Session ' + session)
            plt.xlim(min, max)

            # plt.show()
            plt.savefig(directory + os.sep +session+'graph.png')
