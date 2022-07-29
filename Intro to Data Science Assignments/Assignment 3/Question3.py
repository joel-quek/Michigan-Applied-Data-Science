def answer_three():
    data_info = answer_one()
    avgGDP = data_info[['2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']].mean(axis=1).sort_values(ascending=False)
    return avgGDP