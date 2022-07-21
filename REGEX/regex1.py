# https://docs.python.org/3/library/re.html

'''
What is the correct regular expression to match a URL with letters, numbers, underscores and dots? A valid URL defined in this problem must meet the following requirements:

The URL consists of two or more strings made of letters, numbers, and underscores.
A dot is used in between the strings.
No two dots are allowed to appear consecutively.
For example, your regex should match URLs like: www.aBC.com, abc.com, ab_c.de8f.com
But your regex should not match: abc, abc..com
'''

(\w+\.)+\w+