import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd

linear_data = np.array([1,2,3,4,5,6,7,8])
quadratic_data = linear_data**2

plt.figure()
# plt.plot(linear_data, '-o', quadratic_data, '-o')
# plt.plot([22,44,55], '--r')
'''
plt.xlabel('Some data')
plt.ylabel('Some other data')
plt.title('A title')
plt.legend(['Baseline', 'Competition'])
'''
# ------------------------------------------------
# plt.gca().fill_between(range(len(linear_data)), linear_data, quadratic_data, facecolor="blue", alpha = 0.25)
# what is GCA? GCA = Get Current Axis. Apparently it is some parameter of the PLT object (https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.gca.html)
# alpha is the tranparency value
# ------------------------------------------------
observation_dates = np.arange('2017-01-01', '2017-01-09', dtype = 'datetime64[D]')
observation_dates = list(map(pd.to_datetime, observation_dates))
plt.plot(observation_dates, linear_data, '-o', observation_dates, quadratic_data, '-o')
#-----------------------------------------------------------------
# We need to adjust the angles of the axis labels
x = plt.gca().xaxis

for item in x.get_ticklabels():
    item.set_rotation(45)

plt.subplots_adjust(bottom=0.25)
# -----------------------------------------------------------------
ax = plt.gca()
ax.set_xlabel('Date')
ax.set_ylabel('Units')
ax.set_title("Quadratic($x^2$) vs. Linear ($x$) performance") #LaTex functionality
# ------------------------------------------------------------------
plt.show()