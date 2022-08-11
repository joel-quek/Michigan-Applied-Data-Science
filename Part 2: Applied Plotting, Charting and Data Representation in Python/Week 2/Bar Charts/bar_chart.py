import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
from random import randint

linear_data = np.array([1,2,3,4,5,6,7,8])
quadratic_data = linear_data**2
# --------------------------------------------
# First bar
plt.figure()
xvals = range(len(linear_data))
plt.bar(xvals, linear_data, width = 0.3)
# --------------------------------------------
# Second bar
new_xvals = []
for item in xvals:
    new_xvals.append(item+0.3)

plt.bar(new_xvals, quadratic_data, width=0.3, color='red')
# ---------------------------------------------
linear_err = [randint(0,15) for x in range(len(linear_data))] 

# This will plot a new set of bars with errorbars using the list of random error values
plt.bar(xvals, linear_data, width = 0.3, yerr=linear_err)
# What does this section do?
# ---------------------------------------------

plt.show()