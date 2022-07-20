import numpy as np
import math

a = np.array([1,2,3])
print(a.ndim) # this returns the dimension of the array which is 1 dimensional

# A list of lists is multidimensional like a matrix
b = np.array( [ [1,2,3], [4,5,6] ] )
print(b.shape) # this returns the dimensions of the matrix which is row x column
print (b.ndim) # this returns the dimentions only which is 2-dim

