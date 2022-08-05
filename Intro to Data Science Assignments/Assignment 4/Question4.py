import pandas as pd
import numpy as np
import scipy.stats as stats
import re

nfl_df=pd.read_csv("assets/nfl.csv")
cities=pd.read_html("assets/wikipedia_data.html")[1]
cities=cities.iloc[:-1,[0,3,5,6,7,8]]
# For this question, calculate the win/loss ratio's correlation with the population of the city it is in for the NFL using 2018 data.
# https://lfwberhe.labs.coursera.org/files/assignments/assignment4/assets/wikipedia_data.html
# --------------------------------------------------------------------------------------------------------------------------------------
nfldf2 = nfl_df[nfl_df["year"]==2018] #clean up csv data
nfldf2.drop([0,5,10,15,20,25,30,35], axis=0, inplace=True) # remove rows 2, 7, 12, 17, 22, 27, 32, 37
nfldf2 = nfldf2[["team", "W-L%"]]
nfldf2['team'] = nfldf2['team'].str.replace('(\([0-9]*[0-9]*\))$','', regex=True)
nfldf2['team'] = nfldf2['team'].str.replace('*','', regex=True)
nfldf2['team'] = nfldf2['team'].str.replace('+','', regex=True)
nfldf2.rename(columns={'team':'Area and NFL Team'}, inplace=True)
nfldf2.rename(columns={'W-L%':'WL Ratio'}, inplace=True)
nfldf2=nfldf2.astype({'Area and NFL Team': str})
nfldf2['Area and NFL Team'] = nfldf2['Area and NFL Team'].str.rstrip()
nfldf2 = nfldf2.astype({'Area and NFL Team': str,'WL Ratio': float})
nfldf2['NFL Team']=nfldf2['Area and NFL Team'].str.extract('([0-9]*[0-9]*[A-Z]*[a-z]+$)') #create a column for team names Cannot put [A-Z]*[a-z] as it will only call Sox
# nfldf2 = mlbdf2.sort_values('Area and MLB Team', ascending=False) # Los Angeles and New York are repeated, so that means 28 unique Areas
#print(nfldf2) #output correct and matches teams
#print(len(nfldf2))
# --------------------------------------------------------------------------------------------------------------------------------------
cities2 = cities[["Metropolitan area", "Population (2016 est.)[8]", "NFL"]]
cities2=cities2[cities2['NFL'].str.contains('^[0-9a-zA-Z]', regex=True)] #this means I am pulling out data that starts with letters (AND numbers cos of 76ers). So i exclude those data eg. [note 25]
cities2['NFL'] = cities2['NFL'].str.replace('\[.*\]$','',regex=True) # remove square parentheses like [note 25] and join names together
cities2.sort_values('Metropolitan area', ascending=True)
cities2.rename(columns={'Population (2016 est.)[8]':'Population', 'Metropolitan area':'Area', 'NFL':'NFL Team'}, inplace=True)
    # important line
teams = cities2['NFL Team'].str.extract('(\w{0,1}[a-z0-9]*\ \w{0,1}[a-z0-9]*|\w{0,1}[a-z0-9]*)(\w{0,1}[a-z0-9]*\ \w{0,1}[a-z0-9]*|\w{0,1}[a-z0-9]*)(\w{0,1}[a-z0-9]*\ \w{0,1}[a-z0-9]*|\w{0,1}[a-z0-9]*)')
teams[['Area']] = cities2[['Area']]
teams = teams.melt(id_vars='Area').drop(columns=['variable']).replace("",np.nan).replace("—",np.nan).dropna().rename(columns={"value":"NFL Team"})
# teams['MLB Team']=teams['MLB Team'].str.replace('\ Sox','Sox', regex=True) # if not red sox and white sox will output sox only
    #important line
teams['NFL Team']=teams['NFL Team'].str.replace('[\w.]*\ ','', regex=True) # keep only the last team name

    # How to pd.melt() youtube video: https://www.youtube.com/watch?v=DCqWZ0DGVqw
teams = pd.merge(teams, cities2, how='left', on = 'Area')
teams = teams[['Area', 'NFL Team_x', 'Population']]
teams.rename(columns={'NFL Team_x':'NFL Team'}, inplace=True)

#print(teams) #output is correct and matches nfldf2
#print(len(teams))
# --------------------------------------------------------------------------------------------------------------------------------------
combined=pd.merge(teams, nfldf2, 'outer', on='NFL Team').dropna()

#combined=combined.groupby('Area').agg({'WLRatio': np.nanmean, 'Population': np.nanmean}) #aggregate data of repeated regions by taking average
combined=combined.drop(columns=['NFL Team','Area and NFL Team'])
combined=combined.sort_values(by='Area')
combined=combined.astype({'Population': int})
combined=combined.astype({'WL Ratio': float})
combined=combined.groupby('Area').agg({'WL Ratio': np.nanmean, 'Population': np.nanmean}) # los angeles and new york populations are not averaged

print(combined)
print(len(combined)) # combined dataframe output is correct
#-------------------------------------------------------------------------------------------------------------------------------
population_by_region = combined['Population'] # pass in metropolitan area population from cities
win_loss_by_region = combined['WL Ratio'] # pass in win/loss ratio from mlb_df in the same order as cities["Metropolitan area"]



print(stats.pearsonr(population_by_region, win_loss_by_region)[0])