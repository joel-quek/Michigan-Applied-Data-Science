import pandas as pd
import numpy as np
import scipy.stats as stats
import re

nba_df=pd.read_csv("assets/nba.csv")
cities=pd.read_html("assets/wikipedia_data.html")[1]
cities=cities.iloc[:-1,[0,3,5,6,7,8]]


nbadf2 = nba_df[nba_df["year"]==2018] #clean up csv data
nbadf2 = nbadf2[["team", "W/L%"]]
nbadf2['team'] = nbadf2['team'].str.replace('(\([0-9]*[0-9]*\))$','', regex=True)
nbadf2['team'] = nbadf2['team'].str.replace('*','', regex=True)
nbadf2.rename(columns={'team':'Area and NBA Team'}, inplace=True)
nbadf2=nbadf2.astype({'Area and NBA Team': str})
nbadf2['Area and NBA Team'] = nbadf2['Area and NBA Team'].str.rstrip()

nbadf2['NBA Team']=nbadf2['Area and NBA Team'].str.extract('([0-9]*[0-9]*[A-Z]*[a-z]+$)') #create a column for team names

#print(nbadf2) # nbadf2 output is correct
#print(len(nbadf2))
# ---------------------------------------------------------------------------------------------------------------------------------------
cities2 = cities[["Metropolitan area", "Population (2016 est.)[8]", "NBA"]]
cities2=cities2[cities2['NBA'].str.contains('^[0-9a-zA-Z]', regex=True)] #this means I am pulling out data that starts with letters (AND numbers cos of 76ers). So i exclude those data eg. [note 25]
cities2['NBA'] = cities2['NBA'].str.replace('\[.*\]$','',regex=True) # remove square parentheses like [note 25] and join names together
cities2.sort_values('Metropolitan area', ascending=True)
cities2.rename(columns={'Population (2016 est.)[8]':'Population', 'Metropolitan area':'Area', 'NBA':'NBA Team'}, inplace=True)
# important line
teams = cities2['NBA Team'].str.extract('(\w{0,1}[a-z0-9]*\ \w{0,1}[a-z0-9]*|\w{0,1}[a-z0-9]*)(\w{0,1}[a-z0-9]*\ \w{0,1}[a-z0-9]*|\w{0,1}[a-z0-9]*)(\w{0,1}[a-z0-9]*\ \w{0,1}[a-z0-9]*|\w{0,1}[a-z0-9]*)')

teams[['Area']] = cities2[['Area']]
teams = teams.melt(id_vars='Area').drop(columns=['variable']).replace("",np.nan).replace("—",np.nan).dropna().rename(columns={"value":"NBA Team"})

#important line
teams['NBA Team']=teams['NBA Team'].str.replace('[\w.]*\ ','', regex=True) # keep only the last team name

# How to pd.melt() youtube video: https://www.youtube.com/watch?v=DCqWZ0DGVqw
teams = pd.merge(teams, cities2, how='left', on = 'Area')
teams = teams[['Area', 'NBA Team_x', 'Population']]
teams.rename(columns={'NBA Team_x':'NBA Team'}, inplace=True)

#print(teams) # teams output is correct
#print(len(teams))
#-------------------------------------------------------------------------------------------------------------------------------------------
combined=pd.merge(teams, nbadf2, 'outer', on='NBA Team').dropna()

#combined=combined.groupby('Area').agg({'WLRatio': np.nanmean, 'Population': np.nanmean}) #aggregate data of repeated regions by taking average
combined=combined.drop(columns=['NBA Team','Area and NBA Team'])
combined=combined.sort_values(by='Area')
combined=combined.astype({'Population': int})
combined=combined.astype({'W/L%': float})
combined=combined.groupby('Area').agg({'W/L%': np.nanmean, 'Population': np.nanmean}) # los angeles and new york populations are not averaged

print(combined)
print(len(combined)) # combined dataframe output is correct

population_by_region = combined['Population'] # pass in metropolitan area population from cities
win_loss_by_region = combined['W/L%'] # pass in win/loss ratio from nhl_df in the same order as cities["Metropolitan area"]

print(stats.pearsonr(population_by_region, win_loss_by_region)[0])
