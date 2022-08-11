# Stacked bar chart

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
from random import randint

linear_data = np.array([1,2,3,4,5,6,7,8])
exponential_data = linear_data**2
# --------------------------------------------

# ---------------------------------------------
# or use barh for horizontal bar charts
plt.figure()
xvals = range(len(linear_data))
plt.barh(xvals, linear_data, height = 0.3, color='b')
plt.barh(xvals, exponential_data, height = 0.3, left=linear_data, color='r')

plt.show()