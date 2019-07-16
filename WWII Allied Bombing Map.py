import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import time
from matplotlib.animation import FuncAnimation
import matplotlib.animation
import sys
import datetime
from matplotlib import gridspec
from matplotlib import colors
#from mpl_toolkits.basemap import Basemap



#included for reference: previous matplotlib => video script
#handy variables  Note:  10/7/2018 download

#max lat, long:  58.05, 38.35
#min lat, long: 30.335, -10.36
max_lat = 58.05
max_long = 38.35
min_lat = 30.335
min_long = -10.36

rawdf = pd.read_csv('THOR_WWII_DATA_CLEAN.csv', usecols=['MSNDATE', 'LATITUDE', 'LONGITUDE', 'TOTAL_TONS'],
                    parse_dates=['MSNDATE'])


rawdf = rawdf.dropna(subset=['MSNDATE','LATITUDE', 'LONGITUDE', 'TOTAL_TONS'])


filterdf = rawdf[(rawdf["LATITUDE"] > min_lat) & (rawdf["LATITUDE"] < max_lat) & (rawdf["LONGITUDE"] > min_long) &
                 (rawdf["LONGITUDE"] < max_long) & (rawdf["TOTAL_TONS"] != 0)]

min_date = datetime.datetime(year=1943, month=1, day=1) #filterdf["MSNDATE"].min()
max_date = datetime.datetime(year=1945, month=7, day=1) #filterdf["MSNDATE"].max()
explosion_days = 10

run_time = (max_date - min_date).days + explosion_days
print('runtime:')
print(run_time)

explosions_df = filterdf
explosions_df['Timeshift'] = 0
print(explosions_df.shape)

for i in range(1,explosion_days):
    explosionsadder_df = filterdf
    explosionsadder_df['TOTAL_TONS'] = filterdf['TOTAL_TONS'] *(explosion_days-i)/explosion_days
    explosionsadder_df['Timeshift'] = i
    explosionsadder_df["MSNDATE"] = explosionsadder_df["MSNDATE"]-datetime.timedelta(days=i)
    explosions_df = explosions_df.append(explosionsadder_df)








filterdf = filterdf.set_index('MSNDATE')
explosions_df = explosions_df.set_index('MSNDATE')
print(explosions_df.info())
print(explosions_df.head())

fig = plt.figure()
fig.set_facecolor('black')
europemap = fig.add_subplot(111)
basemap = plt.imread('Background map image.png')





def timedecorator(func):
    def time_wrapper(x):
        timestart = time.clock()
        print("  calling  " + func.__name__)
        func(x)
        elapsedtime = time.clock() - timestart
        print(str(elapsedtime*1000) + "Milliseconds elapsed running " + func.__name__)
    return time_wrapper

@timedecorator
def gifupdate(j):
    plt.clf()
    fig.set_facecolor('black')
    europemap = fig.add_subplot(111)
    img_datetime = min_date+datetime.timedelta(days=j)
    print(str(img_datetime.date()))
    plt.xlim(min_long, max_long)
    plt.ylim(min_lat, max_lat)
    plt.axis('off')
    plt.imshow(basemap, aspect='auto', extent=(min_long, max_long, min_lat, max_lat))
    dailydf = explosions_df.loc[str(img_datetime.date())]
    europemap.scatter(dailydf['LONGITUDE'], dailydf['LATITUDE'], s=dailydf['TOTAL_TONS']*3, alpha=.25, color='orange')

    fig.set_facecolor('black')
    fig.patch.set_facecolor('black')
    plt.tight_layout()
    europemap.text(.5, .9, 'WWII Allied Bombing: '+str(img_datetime.date()),
            horizontalalignment='center',
            transform=europemap.transAxes, fontdict={'family': 'serif',
        'color':  'red',
        'weight': 'normal',
        'size': 16,
        })
    return fig


if __name__ == '__main__':
    anim = FuncAnimation(fig, gifupdate, frames=run_time, interval=1, repeat=False)
    #note, imagemagick must be installed on your machine or ffmpeg, depending on which writer you choose
    anim.save('bombing2.mpeg', dpi=400, writer='imagemagick',fps=15,)

    plt.show()



