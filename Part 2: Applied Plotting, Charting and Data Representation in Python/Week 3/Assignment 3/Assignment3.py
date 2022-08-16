import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

np.random.seed(12345)

df = pd.DataFrame([np.random.normal(32000,200000,3650), 
                   np.random.normal(43000,100000,3650), 
                   np.random.normal(43500,140000,3650), 
                   np.random.normal(48000,70000,3650)], 
                  index=[1992,1993,1994,1995])

# print(df.shape) # 4 rows and 3650 columns
# ---------------------------------------------------------------------------------------------------------------------
# Source: https://pythonforundergradengineers.com/python-matplotlib-error-bars.html
# ----------------------------------------------------------------------------------------------------------------------
years = [1992,1993,1994,1995]
year_mean = df.mean(axis = 1) # mean according to columns. This is a pandas series indexed by the years.
s_d = df.std(axis = 1) # sd according to columns. This is a pandas series indexed by the years.
yerr = s_d / np.sqrt(df.shape[1]) * stats.t.ppf(0.95, df.shape[1]-1) # what is the basis of this?
#print(year_mean)
#print(s_d)
#print(yerr)

# -----------------------------------------------------------------------------------------------------------------------
x_pos = np.arange(len(years))
means = [year_mean.loc[1992],year_mean.loc[1993],year_mean.loc[1994],year_mean.loc[1995]]
sds = [s_d.loc[1992],s_d.loc[1993],s_d.loc[1994],s_d.loc[1995]] # the list of standard deviations. These are not the errors
yerrs = [yerr.loc[1992],yerr.loc[1993],yerr.loc[1994],yerr.loc[1995]]
#print(x_pos)
#print(means)
#print(sds)
# ------------------------------------------------------------------------------------------------------------------------
fig, ax = plt.subplots()
ax.bar(x_pos, means, yerr=yerrs, align='center', alpha=0.5, ecolor='black', capsize=10)
ax.set_ylabel('Coefficient of Thermal Expansion ($\degree C^{-1}$)')
ax.set_xticks(x_pos)
ax.set_xticklabels(years)
ax.set_title('Coefficent of Thermal Expansion (CTE) of Three Metals')
ax.yaxis.grid(True)

# Save the figure and show
plt.tight_layout()
plt.savefig('bar_plot_with_error_bars.png')
plt.show()
