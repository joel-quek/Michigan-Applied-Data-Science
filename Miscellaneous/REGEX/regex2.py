'''
Answer for Question 6
What is the correct regular expression to match an ISBN number from two publishers (World Scientific from Singapore, and Sigma Publications from Greece)? A valid ISBN code defined in this problem must meet the following requirements:

The ISBN number consists of 10 digits, with dashes(-) in between.
The ISBN number must match the patterns of one of the following publishers(x means a digit from 0 to 9): for World Scientific, the pattern should be xxxx-x-xxxx-x, and for Sigma Publications, the pattern should be xxx-xxx-xxx-x.
For example, your regex should match ISBNs like: 9971-5-0210-0, 960-425-059-0

'''

\d{4}-\d-\d{4}-\d|\d{3}-\d{3}-\d{3}-\d