import csv
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Play with data here


impactful_stock_dates = {}
price_diff_normalised = []

impactful_headlines = {}

numOfPoints = 0

fileName = "price_difference_normalised_fb.csv"

# Read data
with open(fileName, 'r', encoding='utf-8') as csvfile:
        rawData = csv.reader(csvfile, delimiter=',')
        # Append data
        for row in rawData:
            if(row[0] == 'Date'):
                continue
            price_value = row[1]
            price_diff_normalised.append(price_value)
            if(float(price_value) > 0.5 or float(price_value) < -0.5 ):
                numOfPoints += 1
                date = row[0] # Date
                if(float(price_value) < 0): # Negative
                    impactful_stock_dates[date] = 'Negative'
                else:
                    impactful_stock_dates[date] = 'Positive'
                    
# Read data
with open('headlines_non_empty_fb.csv', 'r', encoding='utf-8') as csvfile:
        rawData = csv.reader(csvfile, delimiter=',')
        # Append data
        for row in rawData:
            if(row[0] == 'Date'):
                continue
            date = row[0]
            headline = row[1]
            if(date in impactful_stock_dates):
                impactful_headlines[headline] = impactful_stock_dates[date]

#impactful_stock_dates_pandas = pd.to_datetime(impactful_stock_dates)

print("Positive Points Total: " + str(numOfPoints))
print("Percentage: " + str((numOfPoints) * 100 / (len(price_diff_normalised))))
print('\n')

for headline in impactful_headlines:
    sentiment = ''
    if(impactful_headlines[headline] == 'Negative'):
        sentiment = '--'
    else:
        sentiment = '++'
    print(headline + " " + sentiment)

#fig = plt.figure(figsize=(10,6))
#plt.scatter(impactful_stock_dates_pandas, high_low_values)
#plt.title("Pls help")
#plt.show()