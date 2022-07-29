def answer_seven():
    df = answer_one()
    df['self to total'] = df['Self-citations']/df['Citations']
    df.sort_values(['self to total'], ascending=False, inplace=True)
    best=df.iloc[0]
    country=best.name
    max_cite = best['self to total']
    return(country,max_cite)