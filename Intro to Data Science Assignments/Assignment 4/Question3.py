import pandas as pd
import numpy as np
import scipy.stats as stats
import re

# For this question, calculate the win/loss ratio's correlation with the population of the city it is in for the MLB using 2018 data.
# https://lfwberhe.labs.coursera.org/files/assignments/assignment4/assets/wikipedia_data.html
mlb_df=pd.read_csv("assets/mlb.csv")
cities=pd.read_html("assets/wikipedia_data.html")[1]
cities=cities.iloc[:-1,[0,3,5,6,7,8]]
#-------------------------------------------------------------------------------------------------------------------------------
mlbdf2 = mlb_df[mlb_df["year"]==2018] #clean up csv data
mlbdf2['team'] = mlbdf2['team'].str.replace('\ Sox','Sox', regex=True) # prevent sole 'sox' output
mlbdf2 = mlbdf2[["team", "W-L%"]]
mlbdf2['team'] = mlbdf2['team'].str.replace('(\([0-9]*[0-9]*\))$','', regex=True)
mlbdf2['team'] = mlbdf2['team'].str.replace('*','', regex=True)
mlbdf2.rename(columns={'team':'Area and MLB Team'}, inplace=True)
mlbdf2.rename(columns={'W-L%':'WL Ratio'}, inplace=True)
mlbdf2=mlbdf2.astype({'Area and MLB Team': str})
mlbdf2['Area and MLB Team'] = mlbdf2['Area and MLB Team'].str.rstrip()
#print(mlbdf2)
#print(len(mlbdf2))
mlbdf2['MLB Team']=mlbdf2['Area and MLB Team'].str.extract('([A-Za-z]+$)') #create a column for team names Cannot put [A-Z]*[a-z] as it will only call Sox
# mlbdf2 = mlbdf2.sort_values('Area and MLB Team', ascending=False) # Los Angeles and New York are repeated, so that means 28 unique Areas
#print(mlbdf2) #output correct and matches teams
#print(len(mlbdf2))
#-------------------------------------------------------------------------------------------------------------------------------
cities2 = cities[["Metropolitan area", "Population (2016 est.)[8]", "MLB"]]
cities2=cities2[cities2['MLB'].str.contains('^[0-9a-zA-Z]', regex=True)] #this means I am pulling out data that starts with letters (AND numbers cos of 76ers). So i exclude those data eg. [note 25]
cities2['MLB'] = cities2['MLB'].str.replace('\[.*\]$','',regex=True) # remove square parentheses like [note 25] and join names together
cities2.sort_values('Metropolitan area', ascending=True)
cities2.rename(columns={'Population (2016 est.)[8]':'Population', 'Metropolitan area':'Area', 'MLB':'MLB Team'}, inplace=True)
    # important line
teams = cities2['MLB Team'].str.extract('(\w{0,1}[a-z0-9]*\ \w{0,1}[a-z0-9]*|\w{0,1}[a-z0-9]*)(\w{0,1}[a-z0-9]*\ \w{0,1}[a-z0-9]*|\w{0,1}[a-z0-9]*)(\w{0,1}[a-z0-9]*\ \w{0,1}[a-z0-9]*|\w{0,1}[a-z0-9]*)')
teams[['Area']] = cities2[['Area']]
teams = teams.melt(id_vars='Area').drop(columns=['variable']).replace("",np.nan).replace("—",np.nan).dropna().rename(columns={"value":"MLB Team"})
teams['MLB Team']=teams['MLB Team'].str.replace('\ Sox','Sox', regex=True) # if not red sox and white sox will output sox only
    #important line
teams['MLB Team']=teams['MLB Team'].str.replace('[\w.]*\ ','', regex=True) # keep only the last team name

    # How to pd.melt() youtube video: https://www.youtube.com/watch?v=DCqWZ0DGVqw
teams = pd.merge(teams, cities2, how='left', on = 'Area')
teams = teams[['Area', 'MLB Team_x', 'Population']]
teams.rename(columns={'MLB Team_x':'MLB Team'}, inplace=True)

#print(teams) #output is correct and matches mlbdf2
#print(len(teams))
#-------------------------------------------------------------------------------------------------------------------------------
combined=pd.merge(teams, mlbdf2, 'outer', on='MLB Team').dropna()

#combined=combined.groupby('Area').agg({'WLRatio': np.nanmean, 'Population': np.nanmean}) #aggregate data of repeated regions by taking average
combined=combined.drop(columns=['MLB Team','Area and MLB Team'])
combined=combined.sort_values(by='Area')
combined=combined.astype({'Population': int})
combined=combined.astype({'WL Ratio': float})
combined=combined.groupby('Area').agg({'WL Ratio': np.nanmean, 'Population': np.nanmean}) # los angeles and new york populations are not averaged

print(combined)
print(len(combined)) # combined dataframe output is correct

#-------------------------------------------------------------------------------------------------------------------------------
population_by_region = combined['Population'] # pass in metropolitan area population from cities
win_loss_by_region = combined['WL Ratio'] # pass in win/loss ratio from mlb_df in the same order as cities["Metropolitan area"]

# assert len(population_by_region) == len(win_loss_by_region), "Q3: Your lists must be the same length"
# assert len(population_by_region) == 26, "Q3: There should be 26 teams being analysed for MLB"

print(stats.pearsonr(population_by_region, win_loss_by_region)[0])