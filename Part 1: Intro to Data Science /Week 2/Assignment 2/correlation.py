import numpy as np
import pandas as pd
#import scipy.stats as stats
   
# df = pd.read_csv("assets/NISPUF17.csv", index_col=0)
df = pd.read_csv('week_2_assignment/cdc.csv', index_col=0)
cpox_vax = df[['HAD_CPOX', 'P_NUMVRC']]
cpox_vax2 = cpox_vax[cpox_vax['HAD_CPOX'].lt(3)].dropna()
cpox_vax2.columns = ["had_chickenpox_column", "num_chickenpox_vaccine_column"]
print(cpox_vax2)
