import csv
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

stock_dates = []
high_low_values = []

fileName = "price_high_low.csv"

# Read data
with open(fileName, 'r', encoding='utf-8') as csvfile:
        rawData = csv.reader(csvfile, delimiter=',')
        # Append data
        for row in rawData:
            if(row[0] == 'Date'):
                continue
            stock_dates.append(row[0]) # Date
            high_low_values.append(row[1])

stock_dates_pandas = pd.to_datetime(stock_dates)

fig = plt.figure(figsize=(10,6))
plt.scatter(stock_dates_pandas, high_low_values)
plt.title("Pls help")
plt.show()