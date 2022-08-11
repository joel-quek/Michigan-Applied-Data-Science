import matplotlib as mpl
import matplotlib.pyplot as plt

plt.figure()
plt.plot(3,2, 'o')
ax=plt.gca()
ax.axis([0,6,0,10])
plt.show()