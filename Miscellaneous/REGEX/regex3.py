'''What is the correct regular expression to match a DOI registered by Crossref? A valid DOI(e.g. doi:10.1038/nphys1170) defined in this problem must meet the following requirements:

The DOI starts with doi:
The link has two parts divided by a “/”. In the first part, there can only be numbers and dots, and in the second part, there can be any characters. There should be at least one character in each part.
For example, your regex should match DOIs like: doi:10.1038/nphys1170, doi:10.1002/0470841559.ch1

One possible solution:
'''

doi:[\d.]+/.+