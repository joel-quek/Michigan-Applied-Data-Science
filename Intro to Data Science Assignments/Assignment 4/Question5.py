'''
In this question I would like you to explore the hypothesis
---------------------------------------------------------------------------
that given that an area has two sports teams in different sports,
those teams will perform the same within their respective sports. => ie their average WL% will be the same/small margin of differene.
=> This is the NULL HYPOTHESIS
--------------------------------------------------------------------------
How I would like to see this explored is with a series of
paired t-tests (so use ttest_rel) between all pairs of sports.
=> The ttest is done pariwise on the sports themselves, and not the regions. So we need sort of a 4x4 table to check all pairwise p-values
--------------------------------------------------------------------------
Are there any sports where we can reject the null hypothesis?
=> insofar as there is a 4X4 table, I think we only care about 4 values, the diagonal values.
Again, average values where a sport has multiple teams in one region.
--------------------------------------------------------------------------
Remember, you will only be including, for each sport, cities which have teams engaged in that sport, drop others as appropriate.
=> if the city does not have a team in a sport, then heck it lah
--------------------------------------------------------------------------
This question is worth 20% of the grade for this assignment.
=> pass already, the 20% dont care. Just do for fun
'''
import pandas as pd
import numpy as np
import scipy.stats as stats
import re

mlb_df=pd.read_csv("assets/mlb.csv")
nhl_df=pd.read_csv("assets/nhl.csv")
nba_df=pd.read_csv("assets/nba.csv")
nfl_df=pd.read_csv("assets/nfl.csv")
cities=pd.read_html("assets/wikipedia_data.html")[1]
cities=cities.iloc[:-1,[0,3,5,6,7,8]]

# --------------------------------------------------------------------
def nhl_wl():
    nhldf2 = nhl_df[nhl_df["year"]==2018]
    nhldf2 = nhldf2[["team", "W", "L"]]

    nhldf2.drop([0,9,18,26], axis=0, inplace=True)
    nhldf2['W']=nhldf2['W'].astype('int')
    nhldf2['L']=nhldf2['L'].astype('int')
    nhldf2['WLRatio']=nhldf2['W']/(nhldf2["W"]+nhldf2["L"])
    nhldf2['team'] = nhldf2['team'].str.replace('\*$','', regex=True)
    nhldf2.drop(['W','L'], axis=1, inplace=True)
    nhldf2.rename(columns={'team':'Area and NHL Team'}, inplace=True)
    nhldf2['NHL Team']=nhldf2['Area and NHL Team'].str.extract('([A-Z]+[a-z]+$)')

    cities2 = cities[["Metropolitan area", "Population (2016 est.)[8]", "NHL"]]
    cities2=cities2[cities2['NHL'].str.contains('^[a-zA-Z]', regex=True)] #this means I am pulling out data that starts with letters. So i exclude those data eg. [note 25]
    cities2['NHL'] = cities2['NHL'].str.replace('\[.*\]$','',regex=True) # remove square parentheses like [note 25] and join names together
    cities2.sort_values('Metropolitan area', ascending=True)
    cities2.rename(columns={'Population (2016 est.)[8]':'Population', 'Metropolitan area':'Area', 'NHL':'NHL Team'}, inplace=True)

    teams = cities2['NHL Team'].str.extract('(\w{0,1}[a-z0-9]*\ \w{0,1}[a-z0-9]*|\w{0,1}[a-z0-9]*)(\w{0,1}[a-z0-9]*\ \w{0,1}[a-z0-9]*|\w{0,1}[a-z0-9]*)(\w{0,1}[a-z0-9]*\ \w{0,1}[a-z0-9]*|\w{0,1}[a-z0-9]*)')
    teams[['Area']] = cities2[['Area']]
    teams = teams.melt(id_vars='Area').drop(columns=['variable']).replace("",np.nan).replace("—",np.nan).dropna().rename(columns={"value":"NHL Team"})

    teams['NHL Team']=teams['NHL Team'].str.replace('[\w.]*\ ','', regex=True) # keep only the last team name

    teams = pd.merge(teams, cities2, how='left', on = 'Area')
    teams = teams[['Area', 'NHL Team_x', 'Population']]
    teams.rename(columns={'NHL Team_x':'NHL Team'}, inplace=True)

    combined=pd.merge(teams, nhldf2, 'outer', on='NHL Team').dropna()
    combined=combined.drop(columns=['NHL Team','Area and NHL Team'])
    combined=combined.sort_values(by='Area')
    combined=combined.astype({'Population': int})
    combined=combined.groupby('Area').agg({'WLRatio': np.nanmean, 'Population': np.nanmean}) # los angeles and new york populations are not averaged
    combined=combined.drop(columns=['Population']) #only keep the WLRatio column
    combined.rename(columns={'WLRatio':'WL Ratio'}, inplace=True) # make all WL Ratio coluns the same name
    return combined
# print(nhl_wl())
# ---------------------------------------------------------------------------------------------------------------------------------------
def nba_wl():
    nbadf2 = nba_df[nba_df["year"]==2018] #clean up csv data
    nbadf2 = nbadf2[["team", "W/L%"]]
    nbadf2['team'] = nbadf2['team'].str.replace('(\([0-9]*[0-9]*\))$','', regex=True)
    nbadf2['team'] = nbadf2['team'].str.replace('*','', regex=True)
    nbadf2.rename(columns={'team':'Area and NBA Team'}, inplace=True)
    nbadf2=nbadf2.astype({'Area and NBA Team': str})
    nbadf2['Area and NBA Team'] = nbadf2['Area and NBA Team'].str.rstrip()

    nbadf2['NBA Team']=nbadf2['Area and NBA Team'].str.extract('([0-9]*[0-9]*[A-Z]*[a-z]+$)') #create a column for team names


    cities2 = cities[["Metropolitan area", "Population (2016 est.)[8]", "NBA"]]
    cities2=cities2[cities2['NBA'].str.contains('^[0-9a-zA-Z]', regex=True)] #this means I am pulling out data that starts with letters (AND numbers cos of 76ers). So i exclude those data eg. [note 25]
    cities2['NBA'] = cities2['NBA'].str.replace('\[.*\]$','',regex=True) # remove square parentheses like [note 25] and join names together
    cities2.sort_values('Metropolitan area', ascending=True)
    cities2.rename(columns={'Population (2016 est.)[8]':'Population', 'Metropolitan area':'Area', 'NBA':'NBA Team'}, inplace=True)

    teams = cities2['NBA Team'].str.extract('(\w{0,1}[a-z0-9]*\ \w{0,1}[a-z0-9]*|\w{0,1}[a-z0-9]*)(\w{0,1}[a-z0-9]*\ \w{0,1}[a-z0-9]*|\w{0,1}[a-z0-9]*)(\w{0,1}[a-z0-9]*\ \w{0,1}[a-z0-9]*|\w{0,1}[a-z0-9]*)')

    teams[['Area']] = cities2[['Area']]
    teams = teams.melt(id_vars='Area').drop(columns=['variable']).replace("",np.nan).replace("—",np.nan).dropna().rename(columns={"value":"NBA Team"})

    teams['NBA Team']=teams['NBA Team'].str.replace('[\w.]*\ ','', regex=True) # keep only the last team name
    teams = pd.merge(teams, cities2, how='left', on = 'Area')
    teams = teams[['Area', 'NBA Team_x', 'Population']]
    teams.rename(columns={'NBA Team_x':'NBA Team'}, inplace=True)

    combined=pd.merge(teams, nbadf2, 'outer', on='NBA Team').dropna()
    combined=combined.drop(columns=['NBA Team','Area and NBA Team'])
    combined=combined.sort_values(by='Area')
    combined=combined.astype({'Population': int})
    combined=combined.astype({'W/L%': float})
    combined=combined.groupby('Area').agg({'W/L%': np.nanmean, 'Population': np.nanmean}) # los angeles and new york populations are not averaged
    combined=combined.drop(columns=['Population'])
    combined.rename(columns={'W/L%':'WL Ratio'}, inplace=True)
    return(combined)
# print(nba_wl())
# ---------------------------------------------------------------------------------------------------------------------------------------
def mlb_wl():
    mlbdf2 = mlb_df[mlb_df["year"]==2018] #clean up csv data
    mlbdf2['team'] = mlbdf2['team'].str.replace('\ Sox','Sox', regex=True) # prevent sole 'sox' output
    mlbdf2 = mlbdf2[["team", "W-L%"]]
    mlbdf2['team'] = mlbdf2['team'].str.replace('(\([0-9]*[0-9]*\))$','', regex=True)
    mlbdf2['team'] = mlbdf2['team'].str.replace('*','', regex=True)
    mlbdf2.rename(columns={'team':'Area and MLB Team'}, inplace=True)
    mlbdf2.rename(columns={'W-L%':'WL Ratio'}, inplace=True)
    mlbdf2=mlbdf2.astype({'Area and MLB Team': str})
    mlbdf2['Area and MLB Team'] = mlbdf2['Area and MLB Team'].str.rstrip()

    mlbdf2['MLB Team']=mlbdf2['Area and MLB Team'].str.extract('([A-Za-z]+$)') #create a column for team names Cannot put [A-Z]*[a-z] as it will only call Sox

    cities2 = cities[["Metropolitan area", "Population (2016 est.)[8]", "MLB"]]
    cities2=cities2[cities2['MLB'].str.contains('^[0-9a-zA-Z]', regex=True)] #this means I am pulling out data that starts with letters (AND numbers cos of 76ers). So i exclude those data eg. [note 25]
    cities2['MLB'] = cities2['MLB'].str.replace('\[.*\]$','',regex=True) # remove square parentheses like [note 25] and join names together
    cities2.sort_values('Metropolitan area', ascending=True)
    cities2.rename(columns={'Population (2016 est.)[8]':'Population', 'Metropolitan area':'Area', 'MLB':'MLB Team'}, inplace=True)
    teams = cities2['MLB Team'].str.extract('([A-Z]{0,2}[a-z0-9]*\ [A-Z]{0,2}[a-z0-9]*|[A-Z]{0,2}[a-z0-9]*)([A-Z]{0,2}[a-z0-9]*\ [A-Z]{0,2}[a-z0-9]*|[A-Z]{0,2}[a-z0-9]*)([A-Z]{0,2}[a-z0-9]*\ [A-Z]{0,2}[a-z0-9]*|[A-Z]{0,2}[a-z0-9]*)')
    teams[['Area']] = cities2[['Area']]
    teams = teams.melt(id_vars='Area').drop(columns=['variable']).replace("",np.nan).replace("—",np.nan).dropna().rename(columns={"value":"MLB Team"})
    teams['MLB Team']=teams['MLB Team'].str.replace('\ Sox','Sox', regex=True) # if not red sox and white sox will output sox only
    teams['MLB Team']=teams['MLB Team'].str.replace('[\w.]*\ ','', regex=True) # keep only the last team name

    teams = pd.merge(teams, cities2, how='left', on = 'Area')
    teams = teams[['Area', 'MLB Team_x', 'Population']]
    teams.rename(columns={'MLB Team_x':'MLB Team'}, inplace=True)

    combined=pd.merge(teams, mlbdf2, 'outer', on='MLB Team').dropna()
    combined=combined.drop(columns=['MLB Team','Area and MLB Team'])
    combined=combined.sort_values(by='Area')
    combined=combined.astype({'Population': int})
    combined=combined.astype({'WL Ratio': float})
    combined=combined.groupby('Area').agg({'WL Ratio': np.nanmean, 'Population': np.nanmean}) # los angeles and new york populations are not averaged
    combined=combined.drop(columns=['Population'])
    return combined
# print(mlb_wl())
# ---------------------------------------------------------------------------------------------------------------------------------------
def nfl_wl():
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

    cities2 = cities[["Metropolitan area", "Population (2016 est.)[8]", "NFL"]]
    cities2=cities2[cities2['NFL'].str.contains('^[0-9a-zA-Z]', regex=True)] #this means I am pulling out data that starts with letters (AND numbers cos of 76ers). So i exclude those data eg. [note 25]
    cities2['NFL'] = cities2['NFL'].str.replace('\[.*\]$','',regex=True) # remove square parentheses like [note 25] and join names together
    cities2.sort_values('Metropolitan area', ascending=True)
    cities2.rename(columns={'Population (2016 est.)[8]':'Population', 'Metropolitan area':'Area', 'NFL':'NFL Team'}, inplace=True)
    teams = cities2['NFL Team'].str.extract('([A-Z]{0,2}[a-z0-9]*\ [A-Z]{0,2}[a-z0-9]*|[A-Z]{0,2}[a-z0-9]*)([A-Z]{0,2}[a-z0-9]*\ [A-Z]{0,2}[a-z0-9]*|[A-Z]{0,2}[a-z0-9]*)([A-Z]{0,2}[a-z0-9]*\ [A-Z]{0,2}[a-z0-9]*|[A-Z]{0,2}[a-z0-9]*)')
    teams[['Area']] = cities2[['Area']]
    teams = teams.melt(id_vars='Area').drop(columns=['variable']).replace("",np.nan).replace("—",np.nan).dropna().rename(columns={"value":"NFL Team"})
    teams['NFL Team']=teams['NFL Team'].str.replace('[\w.]*\ ','', regex=True) # keep only the last team name

    teams = pd.merge(teams, cities2, how='left', on = 'Area')
    teams = teams[['Area', 'NFL Team_x', 'Population']]
    teams.rename(columns={'NFL Team_x':'NFL Team'}, inplace=True)


    combined=pd.merge(teams, nfldf2, 'outer', on='NFL Team').dropna()
    combined=combined.drop(columns=['NFL Team','Area and NFL Team'])
    combined=combined.sort_values(by='Area')
    combined=combined.astype({'Population': int})
    combined=combined.astype({'WL Ratio': float})
    combined=combined.groupby('Area').agg({'WL Ratio': np.nanmean, 'Population': np.nanmean}) # los angeles and new york populations are not averaged
    combined=combined.drop(columns=['Population'])

    return combined
# print(nfl_wl())
# ---------------------------------------------------------------------------------------------------------------------------------------
# Make sure all four dataframes have the same columns Area and WL Ratio
# ---------------------------------------------------------------------------------------------------------------------------------------
#sports = ['NFL', 'NBA', 'NHL', 'MLB']
#p_values = pd.DataFrame({k:np.nan for k in sports}, index=sports)
# ---------------------------------------------------------------------------------------------------------------------------------------
def sports_team_performance():
    sports = ['NFL', 'NBA', 'NHL', 'MLB'] #given in question
    sports_teams = {'NFL': nfl_wl(), 'NBA': nba_wl(), 'NHL': nhl_wl(), 'MLB': mlb_wl()} #tried to pull out dataframe names using strings, but a dictionary is better
    p_values = pd.DataFrame({k:np.nan for k in sports}, index=sports) #given in question
    for i in sports:
        for j in sports:
            combined = pd.merge( sports_teams[i], sports_teams[j],'inner', on=['Area']) #use the dictionary to call out the dataframe names (cannot be string)
            p_values.loc[i, j]=stats.ttest_rel(combined['WL Ratio_x'],combined['WL Ratio_y'])[1] #the column names must be the same
    return p_values
# ---------------------------------------------------------------------------------------------------------------------------------------
print(sports_team_performance())
# ---------------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------------
