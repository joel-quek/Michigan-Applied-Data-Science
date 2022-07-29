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
# ----------------------------------------------------------------------------------------------------------
def plot_optional():
    # %matplotlib inline
    Top15 = answer_one()
    ax = Top15.plot(x='Rank', y='% Renewable', kind='scatter', 
                    c=['#e41a1c','#377eb8','#e41a1c','#4daf4a','#4daf4a','#377eb8','#4daf4a','#e41a1c',
                       '#4daf4a','#e41a1c','#4daf4a','#4daf4a','#e41a1c','#dede00','#ff7f00'], 
                    xticks=range(1,16), s=6*Top15['2014']/10**10, alpha=.75, figsize=[16,6]);

    for i, txt in enumerate(Top15.index):
        ax.annotate(txt, [Top15['Rank'][i], Top15['% Renewable'][i]], ha='center')
    plt.show()
# ----------------------------------------------------------------------------------------------------------
plot_optional()

'''
 print("This is an example of a visualization that can be created to help understand the data. \
This is a bubble chart showing % Renewable vs. Rank. The size of the bubble corresponds to the countries' \
2014 GDP, and the color corresponds to the continent.")
'''