# Use the following data for this assignment:
%matplotlib notebook

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.stats import sem

np.random.seed(12345)

df = pd.DataFrame(np.c_[np.random.normal(32000,200000,3650), 
                   np.random.normal(43000,100000,3650), 
                   np.random.normal(43500,140000,3650), 
                   np.random.normal(48000,70000,3650)], 
                  columns=[1992,1993,1994,1995])

#Bars
values = df.mean()
#Error Bars 95% confidence
sem = df.sem() * 1.96
#Assumed user given input
y = 39493

colorY = round(y)
colors = []
for value in values:
    if round(value) > colorY:
        colors.append('red')
    elif round(value) < colorY:
        colors.append('blue') 
    else:
        colors.append('grey')

plt.axhline(y=y, zorder=0)
plt.bar(range(len(df.columns)), values,
        yerr=sem, align='center', alpha=0.5, color=colors)
plt.xticks(range(len(df.columns)), df.columns)
plt.title('Assignment 3')
plt.show()