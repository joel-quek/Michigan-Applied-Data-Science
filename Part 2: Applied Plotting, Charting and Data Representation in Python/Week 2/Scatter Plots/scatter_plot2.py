import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

zip_generator = zip([1,2,3,4,5], [6,7,8,9,10])
x= list(zip_generator)

#print(x)

y,z = zip(*x)
#print(y)
#print(z)

plt.figure()
# https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.scatter.html
plt.scatter(y[:2], z[:2], s=100, c='red', label = 'Tall Students') # s represents marker size
plt.scatter(y[2:], z[2:], s=100, c='blue', label = 'Short Students')
#plt.plot([22,44,55], '--r')

plt.xlabel('Some data')
plt.ylabel('Some other data')
plt.title('A title')
plt.legend(['Baseline', 'Competition', 'Us'])
plt.show()