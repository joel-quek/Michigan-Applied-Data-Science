import pandas as pd
import numpy as np
import re  
import matplotlib.pyplot as plt
import matplotlib as mpl

def answer_one():    
    # assets/Energy Indicators.xls
    energy = pd.read_excel('Energy Indicators.xls', header= None, skiprows=18, skipfooter=38) # remove header and footer
    energy.replace('...', np.NaN, inplace=True) # replace .. with np.Nan
    energy.drop(energy.columns[[0,1]], axis=1, inplace=True) # remove first two columns
    energy.columns= ['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable'] # rename columns
    energy['Energy Supply']=energy['Energy Supply'].apply(lambda x: x*1000000) # change from petajoules to gigajoules

    energy['Country'] = energy['Country'].str.replace(r"[0-9]+$","", regex=True) # remove superscripts
    energy['Country'] = energy['Country'].str.replace(r" \(.*\)$","", regex=True)  # remove parentheses


    energy['Country'] = energy['Country'].replace({'Republic of Korea' : 'South Korea',
                                                'United States of America' : 'United States',
                                                'United Kingdom of Great Britain and Northern Ireland':'United Kingdom',
                                                'China, Hong Kong Special Administrative Region':'Hong Kong'}) # replace required country names
    # -------------------------------------------------------------------------------------------------------
    gdp = pd.read_csv('GDP.csv', skiprows=4)
    gdp['Country Name'] = gdp['Country Name'].replace({'Korea, Rep.': 'South Korea', 
                                                        'Iran, Islamic Rep.': 'Iran', 
                                                        'Hong Kong SAR, China' : 'Hong Kong'}) 
    gdp.rename(columns={'Country Name': 'Country'}, inplace=True)
    gdp = gdp.loc[:,['2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015',"Country"]]
    # -------------------------------------------------------------------------------------------------------
    ScimEn = pd.read_excel('scimagojr-3.xlsx') # your file cannot be opened at the same time you are trying to run the code
    # -------------------------------------------------------------------------------------------------------
    # scimagojir-energy-gdp2
    join1 = pd.merge(ScimEn,energy,how="inner",left_on="Country",right_on="Country")
    join1 = join1[join1["Rank"]<=15]

    join2 = pd.merge(join1, gdp, how="inner", left_on='Country', right_on='Country')
    join2 = join2.set_index('Country')
    return join2
# ------------------------------------------------------------------------------------------------------------
# displays the sample size (the number of countries in each continent bin), 
# and the sum, mean, and std deviation for the estimated population of each country.
# This function should return a DataFrame with 
# index named Continent ['Asia', 'Australia', 'Europe', 'North America', 'South America'] 
# and columns ['size', 'sum', 'mean', 'std']

def answer_eleven():
    df = answer_one()
    ContinentDict  = {'China':'Asia', 'United States':'North America', 
                  'Japan':'Asia', 'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 'Canada':'North America', 
                  'Germany':'Europe', 'India':'Asia',
                  'France':'Europe', 'South Korea':'Asia', 
                  'Italy':'Europe', 'Spain':'Europe', 
                  'Iran':'Asia','Australia':'Australia', 'Brazil':'South America'}
    df['PopEst'] = df['Energy Supply'] / df['Energy Supply per Capita']
    #avg = df.mean()
    #sd = df.std()
    #total = df.sum()
    #-------------------------------------------------
    df['Continents'] = pd.Series(ContinentDict)#, name="Country")
    
    return df['Continents'] # Code doesnt work. Too messy.

print(answer_eleven())
# https://thewebdev.info/2022/03/26/how-to-use-groupby-results-to-dictionary-of-lists-with-python-pandas/
# https://pandas.pydata.org/pandas-docs/version/0.17.0/generated/pandas.DataFrame.groupby.html