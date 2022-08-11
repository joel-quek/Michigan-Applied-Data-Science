# Stacked bar chart

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
from random import randint

linear_data = np.array([1,2,3,4,5,6,7,8])
exponential_data = linear_data**2
# --------------------------------------------
'''
# First bar
plt.figure()
xvals = range(len(linear_data))
plt.bar(xvals, linear_data, width = 0.3)
'''
# --------------------------------------------
'''
# Second bar
new_xvals = []
for item in xvals:
    new_xvals.append(item+0.3)

plt.bar(new_xvals, quadratic_data, width=0.3, color='red')
'''
# ---------------------------------------------
# stacked bar charts are also possible
plt.figure()
xvals = range(len(linear_data))
plt.bar(xvals, linear_data, width = 0.3, color='b')
plt.bar(xvals, exponential_data, width = 0.3, bottom=linear_data, color='r')
# ---------------------------------------------

plt.show()