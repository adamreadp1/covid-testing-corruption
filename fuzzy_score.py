import pandas as pd
from fuzzywuzzy import fuzz

grouped_df = pd.read_csv('./grouped.csv')
print(grouped_df)
num_companies = len(grouped_df['company_name'])

df = pd.DataFrame(columns=['company_name', 'num_matches', 'num_jumps', 'max_change'])
for company in grouped_df['company_name']:
    print(company)
    fuzzy_matches = []
    for x in grouped_df['company_name']:
        if fuzz.partial_ratio(company, x) >= 90:
            fuzzy_matches.append(x)
    
    matched_rows = grouped_df.loc[grouped_df['company_name'].isin(fuzzy_matches)]
    mean_prices = matched_rows.mean(axis=0).dropna()

    num_jumps = max_change = 0
    prev_price = mean_prices[0]
    for price in mean_prices:
        if prev_price != price:
            num_jumps += 1
            change = abs((price - prev_price)/prev_price)

            if  change > max_change:
                max_change = change
        
        prev_price = price

    df = df.append({
        'company_name':company, 
        'num_matches':len(fuzzy_matches), 
        'num_jumps': num_jumps,
        'max_change': max_change*100
    }, ignore_index=True)

df.to_csv('risk_score.csv')

normalized_df=(df-df.mean())/df.std()
normalized_df['company_name'] = df['company_name']
normalized_df.to_csv('risk_score_normed.csv')
