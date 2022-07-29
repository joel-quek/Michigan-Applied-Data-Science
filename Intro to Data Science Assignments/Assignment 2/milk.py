# Return a tuple of the average number of influenza vaccines 
# for those children we know received breastmilk as a child and those who know did not.

import pandas as pd
import numpy as np 

df = pd.read_csv('week_2_assignment/cdc.csv', index_col=0)
# df = pd.read_csv("assets/NISPUF17.csv", index_col=0)

# df['CBF_01', 'P_NUMFLU']

shef = df[['CBF_01','P_NUMFLU']] 
# print(df[['CBF_01','P_NUMFLU']])

shef_bf = shef[shef['CBF_01'] == 1].dropna()
shef_nobf = shef[shef['CBF_01'] == 2].dropna()

#average number of vaccines for those who received breastmilk
average1 = np.sum(shef_bf['P_NUMFLU'])/len(shef_bf)
average2 = np.sum(shef_nobf['P_NUMFLU'])/len(shef_nobf)

#print(average1)
#print(average2)

answer = (average1, average2)

print (answer)