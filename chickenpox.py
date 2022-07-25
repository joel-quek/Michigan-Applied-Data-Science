'''
vaxxed and got chicken pox
vaxxed but did not get chicken pox. Return results by sex.

This function should return a dictionary in the form of (use the correct numbers):
    {"male":0.2,
    "female":0.4}
'''

import numpy as np
import pandas as pd
answer = dict()
df = pd.read_csv('week_2_assignment/cdc.csv', index_col=0)
# df = pd.read_csv("assets/NISPUF17.csv", index_col=0)
all_sex = df[['SEX','HAD_CPOX', 'P_NUMVRC']]
guys = all_sex[all_sex['SEX']==1].dropna()
girls = all_sex[all_sex['SEX']==2].dropna()

guys_vax = guys[guys['P_NUMVRC']>0]
girls_vax = girls[girls['P_NUMVRC']>0]

guys_vax_cpox = guys_vax[guys_vax['HAD_CPOX']==1]
guys_vax_nocpox = guys_vax[guys_vax['HAD_CPOX']==2]
guys_avg = len(guys_vax_cpox)/len(guys_vax_nocpox)

girls_vax_cpox = girls_vax[girls_vax['HAD_CPOX']==1]
girls_vax_nocpox = girls_vax[girls_vax['HAD_CPOX']==2]
girls_avg = len(girls_vax_cpox)/len(girls_vax_nocpox)

answer["male"]=guys_avg
answer["female"]=girls_avg
print(answer)


