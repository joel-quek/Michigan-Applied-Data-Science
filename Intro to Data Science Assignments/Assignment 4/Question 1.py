import pandas as pd
import numpy as np
import scipy.stats as stats
import re

nhldf=pd.read_csv("assets/nhl.csv")
cities=pd.read_html("assets/wikipedia_data.html")[1]
cities=cities.iloc[:-1,[0,3,5,6,7,8]]

# Calculate win/loss ratio for NHL using 2018 Data
# Win/Loss ratio refers to the number of wins over the number of wins plus the number of losses.
# I only need data till row 36 and win/loss columns
nhldf2 = nhl_df[nhl_df["year"]==2018] #clean up csv data
nhldf2 = nhldf2[["team", "W", "L"]]
nhldf2.drop([0,9,18,26], axis=0, inplace=True) # remove rows 2, 11, 20, 28
nhldf2['W']=nhldf2['W'].astype('int')
nhldf2['L']=nhldf2['L'].astype('int')
nhldf2['WLRatio']=nhldf2['W']/(nhldf2["W"]+nhldf2["L"])
nhldf2['team'] = nhldf2['team'].str.replace('\*$','', regex=True)
nhldf2.drop(['W','L'], axis=1, inplace=True)
nhldf2.rename(columns={'team':'Area and NHL Team'}, inplace=True)
nhldf2['NHL Team']=nhldf2['Area and NHL Team'].str.extract('([A-Z]+[a-z]+$)') #create a column for team names

#print(nhldf2)
#print(f"There are {len(nhldf2)} rows")

# ---------------------------------------------------------------------------------------------------------------------------------------
cities2 = cities[["Metropolitan area", "Population (2016 est.)[8]", "NHL"]]
cities2=cities2[cities2['NHL'].str.contains('^[a-zA-Z]', regex=True)] #this means I am pulling out data that starts with letters. So i exclude those data eg. [note 25]
cities2['NHL'] = cities2['NHL'].str.replace('\[.*\]$','',regex=True) # remove square parentheses like [note 25] and join names together
cities2.sort_values('Metropolitan area', ascending=True)
cities2.rename(columns={'Population (2016 est.)[8]':'Population', 'Metropolitan area':'Area', 'NHL':'NHL Team'}, inplace=True)
# important line
# teams = cities2['NHL Team'].str.extract('([A-Z]*[a-z0-9]*)([A-Z]*[a-z0-9]*)([A-Z]*[a-z0-9]*)') # separating team names that are stuck together (eg 'KingsDucks') and creating a new pandas dataframe
teams = cities2['NHL Team'].str.extract('([A-Z]{0,2}[a-z0-9]*\ [A-Z]{0,2}[a-z0-9]*|[A-Z]{0,2}[a-z0-9]*)([A-Z]{0,2}[a-z0-9]*\ [A-Z]{0,2}[a-z0-9]*|[A-Z]{0,2}[a-z0-9]*)([A-Z]{0,2}[a-z0-9]*\ [A-Z]{0,2}[a-z0-9]*|[A-Z]{0,2}[a-z0-9]*)')

teams[['Area']] = cities2[['Area']]
teams = teams.melt(id_vars='Area').drop(columns=['variable']).replace("",np.nan).replace("—",np.nan).dropna().rename(columns={"value":"NHL Team"})
#important line
teams['NHL Team']=teams['NHL Team'].str.replace('[\w.]*\ ','', regex=True) # keep only the last team name
# How to pd.melt() youtube video: https://www.youtube.com/watch?v=DCqWZ0DGVqw
teams = pd.merge(teams, cities2, how='left', on = 'Area')
teams = teams[['Area', 'NHL Team_x', 'Population']]
teams.rename(columns={'NHL Team_x':'NHL Team'}, inplace=True)

# print(teams)
#print(f"There are {len(teams)} rows")

combined=pd.merge(teams, nhldf2, 'outer', on='NHL Team').dropna()
#combined=combined.groupby('Area').agg({'WLRatio': np.nanmean, 'Population': np.nanmean}) #aggregate data of repeated regions by taking average
combined=combined.drop(columns=['NHL Team','Area and NHL Team'])
combined=combined.sort_values(by='Area')
combined=combined.astype({'Population': int})
combined=combined.groupby('Area').agg({'WLRatio': np.nanmean, 'Population': np.nanmean}) # los angeles and new york populations are not averaged
print(combined)
print(len(combined))

population_by_region = combined['Population'] # pass in metropolitan area population from cities
win_loss_by_region = combined['WLRatio'] # pass in win/loss ratio from nhl_df in the same order as cities["Metropolitan area"]

print(stats.pearsonr(population_by_region, win_loss_by_region)[0])
'''
def nhl_correlation():
    # YOUR CODE HERE
    # raise NotImplementedError()

    population_by_region = [] # pass in metropolitan area population from cities
    win_loss_by_region = [] # pass in win/loss ratio from nhl_df in the same order as cities["Metropolitan area"]

    # assert len(population_by_region) == len(win_loss_by_region), "Q1: Your lists must be the same length"
    # assert len(population_by_region) == 28, "Q1: There should be 28 teams being analysed for NHL"

    return stats.pearsonr(population_by_region, win_loss_by_region)
    '''