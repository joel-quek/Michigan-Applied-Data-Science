import matplotlib as mpl
import matplotlib.pyplot as plt
import mplleaflet as mpl
import pandas as pd
import csv 
import datetime as dt 
import numpy as np 

'''
Before working on this assignment please read these instructions fully. In the submission area, you will notice that you can click the link to 
Preview the Grading for each step of the assignment. This is the criteria that will be used for peer grading. Please familiarize yourself 
with the criteria before beginning the assignment.

An NOAA dataset has been stored in the file data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv. 
This is the dataset to use for this assignment. 
Note: The data for this assignment comes from a subset of The National Centers for Environmental Information (NCEI) Daily Global Historical 
Climatology Network (GHCN-Daily). The GHCN-Daily is comprised of daily climate records from thousands of land surface stations across the globe.

Each row in the assignment datafile corresponds to a single observation.

The following variables are provided to you:
----------------------------------------------------------------------------------------------------------------------------------------------------------
id : station identification code
date : date in YYYY-MM-DD format (e.g. 2012-01-24 = January 24, 2012)
element : indicator of element type
TMAX : Maximum temperature (tenths of degrees C)
TMIN : Minimum temperature (tenths of degrees C)
value : data value for element (tenths of degrees C)
For this assignment, you must:
----------------------------------------------------------------------------------------------------------------------------------------------------------
Read the documentation and familiarize yourself with the dataset, then write some python code which returns 
a line graph of the record high and record low temperatures by day of the year over the period 2005-2014. 
The area between the record high and record low temperatures for each day should be shaded.
----------------------------------------------------------------------------------------------------------------------------------------------------------
Overlay a scatter of the 2015 data for any points (highs and lows) for which the ten year record (2005-2014) record high or record low was broken in 2015.
Watch out for leap days (i.e. February 29th), it is reasonable to remove these points from the dataset for the purpose of this visualization.
----------------------------------------------------------------------------------------------------------------------------------------------------------
Make the visual nice! Leverage principles from the first module in this course when developing your solution. Consider issues such as 
legends, labels, and chart junk.
The data you have been given is near Ann Arbor, Michigan, United States, and the stations the data comes from are shown on the map below.
'''
'''
def leaflet_plot_stations(binsize, hashid):

    df = pd.read_csv('weather_data.csv'.format(binsize))

    station_locations_by_hash = df[df['hash'] == hashid]

    lons = station_locations_by_hash['LONGITUDE'].tolist()
    lats = station_locations_by_hash['LATITUDE'].tolist()

    plt.figure(figsize=(8,8))

    plt.scatter(lons, lats, c='r', alpha=0.7, s=200)

    return mpl.display()

leaflet_plot_stations(400,'fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89')
'''
# -------------------------------------------------------------------------------------------------------------------------
# Open CSV File
df = pd.read_csv('weather_data.csv')
#print(df.head())
# there are 4 columns ID, Date, Element, Data-Value

df = df.sort_values(by='Date')
df.reset_index
# print(df.head())
#print(len(df)) #Count = 165085
# -------------------------------------------------------------------------------------------------------------------------
# Remove Leap Days from CSV
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
# source: https://stackoverflow.com/questions/33365055/attributeerror-can-only-use-dt-accessor-with-datetimelike-values
df = df[~((df.Date.dt.month == 2) & (df.Date.dt.day == 29))] # removing leap days as per the question
#print(df.head())
#print(len(df)) # Count = 165002
# -------------------------------------------------------------------------------------------------------------------------
# Create Dataframe for Year 2005 to 2014 Data
decade = df[((df['Date'] >= '2005-01-01') & (df['Date'] <= '2014-12-31'))] # this line is redundant as all data points are within 2005-2014
#print(len(decade)) # Count = 151245
# -------------------------------------------------------------------------------------------------------------------------
# Create Dataframe for Year 2015 Data
y2015 = df[(df['Date'] >= '2015-01-01')]
# print(twentyfifteen.head())
#print(len(y2015)) #count = 13757
# -------------------------------------------------------------------------------------------------------------------------
# Create Month and Day columns for Decade Dataframe. For purpose of ordering and sorting according to min/max temperatures
pd.to_datetime(decade['Date'])

# works but causes error in plotting (not anymore!)
# The trick is to reset index for the dataframes before plotting
decade['Month'] = decade.Date.dt.month
decade['Day'] = decade.Date.dt.day

'''
# works but also causes error in plotting
decade['Month'] = pd.DatetimeIndex(decade['Date']).month
decade['Day'] = pd.DatetimeIndex(decade['Date']).day
# https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
'''
'''
# works but also causes error in plotting
# decade['Month'] = decade.loc[0, 'Date'].month
decade['Month'] = decade['Date'].split('-')[1]
decade['Day'] = decade['Date'].split('-')[2]
print(decade)
'''
# -------------------------------------------------------------------------------------------------------------------------
# Extract the max and min temperature values from the decade dataframe
decademax = decade.groupby(['Month','Day']).max() #cant I just group by Date?
decademin = decade.groupby(['Month','Day']).min()
# decademax = decade.groupby(['Date']).max()
# decademin = decade.groupby(['Date']).min()
#print(decademax)
#print(decademin)

# print(decademax.dtypes)
decademax['Data_Value'] = decademax['Data_Value'].astype(float) # Change data type from int64 to float64

decademax = decademax.reset_index() #essential step for plotting
decademin = decademin.reset_index()
# print(decademax.dtypes)
# -------------------------------------------------------------------------------------------------------------------------
# Extract 2015 data for any points (highs and lows) for which the ten year record (2005-2014) record high or record low was broken in 2015

y2015 = y2015.reset_index()
y2015_max = y2015.groupby('Date').max()
y2015_min = y2015.groupby('Date').min()

y2015_max = y2015_max.reset_index() # reset index to avoid ValueError: Can only compare identically-labeled Series objects
y2015_min = y2015_min.reset_index()

rec_high = y2015_max[y2015_max['Data_Value'] > decademax['Data_Value']]
rec_low = y2015_min[y2015_min['Data_Value'] < decademin['Data_Value']]

# print(rec_high.head())
# print(rec_low.head())
# -------------------------------------------------------------------------------------------------------------------------
# Plots 
# Line graph of the record high and record low temperatures by day of the year over the period 2005-2014

plt.figure()  

plt.plot(decademax['Data_Value'], '-' , color ='0.4', zorder =0) # i solved the problem by resetting the damn index!!!!!!!!!!!!!!!!
plt.plot(decademin['Data_Value'], '-', color ='0.8', zorder =0) # having problems plotting using plt.plot
# zorder moves the line to a back layer so the scatter plot can be on the top layer 
# https://stackoverflow.com/questions/37246941/specifying-the-order-of-matplotlib-layers
# decademax['Data_Value'].plot() # https://stackoverflow.com/questions/34391282/how-to-plot-object-type-data-in-pandas
# decademin['Data_Value'].plot()


# -------------------------------------------------------------------------------------------------------------------------
# Scatter of the 2015 data for any points (highs and lows) for which the ten year record (2005-2014) record high or record low was broken in 2015.
plt.scatter(rec_high.index, rec_high['Data_Value'], color ='r', zorder=10)
plt.scatter(rec_low.index, rec_low['Data_Value'], color = 'b', zorder=5)
# -------------------------------------------------------------------------------------------------------------------------
plt.xlabel('Day')
plt.ylabel('Temperature')
plt.title('Temperature between 2005 to 2014 \n and extreme temperatures in 2015')
plt.legend(['Decade High', 'Decade Low', '2015 Record High', '2015 Record Low'])
plt.gca().fill_between(range(len(decademax['Data_Value'])), decademax['Data_Value'], decademin['Data_Value'], facecolor="gray", alpha = 0.25) # moved this here so it doesn't affect the legend and does not need to appear in the legend
# --------------------------------------------------------------------------------------------------------------------------
ax1 = plt.gca()
# ---------Essential --------------------
# Set y tick Labels
axlim = ax1.set_ylim(-380,450)
yticks = pd.Series([-300,0,400])
ax1.set_yticks(yticks)
ylabels = pd.Series(yticks/10).astype(int).astype(str) + ' °C'
ax1.set_yticklabels(ylabels, alpha = 0.6)
# -------------------------------------
# Removing Ticks
ax1.tick_params(axis=u'both', which=u'both',length=0)
# ax2.tick_params(axis=u'both', which=u'both',length=0)
# -------------------------------------
# remove Frame
for spine in ax1.spines:
    ax1.spines[spine].set_visible(False)
plt.show()

