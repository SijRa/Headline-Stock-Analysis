import csv

stock_dates = []
headlines_text = [] 

fileName = "headlines.csv"

def read_data():
    with open(fileName, 'r', encoding='utf-8') as csvfile:
            rawData = csv.reader(csvfile, delimiter=',')
            # Read and Append data
            for row in rawData:
                if(row[0] == 'Date'):
                    continue
                if(row[1] != 'empty'):
                    stock_dates.append(row[0]) # Date
                    headlines_text.append(row[1]) # Headline

def extract_data():
    with open('headlines_non_empty.csv', 'w', encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Date"] + ["Headline"])
            index = 0
            for date in stock_dates:
                writer.writerow([date] + [headlines_text[index]])
                index += 1

read_data()
extract_data()