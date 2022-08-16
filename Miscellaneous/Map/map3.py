# the function
def square(number):
     return number ** 2

# the iterable (or list)  that i want the function to act on
numbers = [1, 2, 3, 4, 5]

# applying the function onto the iterable(or list)
squared = map(square, numbers)


print(list(squared))
# the output: [1, 4, 9, 16, 25]

# map function in a nutshell
# map(f(x), [1, 2, 3, 4, 5]) => [f(1), f(2), f(3), f(4), f(5)]