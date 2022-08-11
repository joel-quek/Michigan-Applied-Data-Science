zip_generator = zip([1,2,3,4,5], [6,7,8,9,10])
x= list(zip_generator)

print(x)

y,z = zip(*x)
print(y)
print(z)