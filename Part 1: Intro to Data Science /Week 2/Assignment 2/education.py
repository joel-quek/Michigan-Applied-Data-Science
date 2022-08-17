import pandas as pd
import numpy as np 

shef = dict()
df = pd.read_csv('week_2_assignment/cdc.csv', index_col=0)

df['EDUC1']

ones = (df['EDUC1']==1).sum()
twos = (df['EDUC1']==2).sum()
threes = (df['EDUC1']==3).sum()
fours = (df['EDUC1']==4).sum()

one = ones/len(df)
two = twos/len(df)
three = threes/len(df)
four = fours/len(df)


shef["less than high school"] = one
shef["high school"] = two
shef["more than high school but not college"] = three
shef["college"] = four

print(shef)

# print(df.head())
# print(df['EDUC1'])