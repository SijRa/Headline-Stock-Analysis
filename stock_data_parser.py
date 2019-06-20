from __future__ import division
import csv

class Stock_Data_Object:
    """
    Data object 
    """
    # Memeber variables
    stock_dates = []
    
    # Opening and Closing Prices
    stock_open_close = []
    price_open_close_normalised = {}

    # Day Highest and Lowest Prices
    stock_high_low = []
    price_high_low_normalied = []

    fileName = ""

    # Constructor
    def __init__(self, fileName):
        self.fileName = fileName 
        with open(fileName + '.csv', 'r') as csvfile:
            rawData = csv.reader(csvfile, delimiter=',', quotechar=',')
            # Read and Append data
            for row in rawData:
                if(row[0] == 'Date'):
                    continue
                self.stock_dates.append(row[0]) # Dates
                # Calculate difference between close and open prices
                price_difference = float(row[4]) - float(row[1])
                self.stock_open_close.append(price_difference)
                # Calculate difference between high and low prices
                range_diff = float(row[2]) - float(row[3])
                self.stock_high_low.append(range_diff)

    def Normalise_Open_Close_Values(self):
        """
        Normalise values to a range between -1,1 
        """
        max_value = max(self.stock_open_close)
        min_value = min(self.stock_open_close)
        index = 0 # Track index of stock_open_close value to use
        for date in self.stock_dates:
            normalised_value = (2 * ((self.stock_open_close[index] - min_value) / (max_value - min_value)) - 1)
            self.price_open_close_normalised[date] = normalised_value
            index += 1
    
    def Normalise_High_Low_Values(self):
        """
        Normalise values to a range between 0,1 
        """
        max_value = max(self.stock_high_low)
        min_value = min(self.stock_high_low)
        for diff in self.stock_high_low:
            normalised_value = ((diff - min_value) / (max_value - min_value))
            self.price_high_low_normalied.append(normalised_value)
        
    def Get_DateColumn(self):
        """
        Returns coloumn with dates for each stock item
        """
        print("Length of stock_dates: %d" % len(self.stock_dates)) 
        return self.stock_dates
    
    def Create_HighLow_CSV(self, highLowList):
        """
        Create csv file using a dictionary (Normalised Prices)
        """
        with open('price_high_low_normalised.csv', 'w', encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Date"] + ["High/Low (Normalised)"])
            index = 0
            for entry in highLowList:
                writer.writerow([self.stock_dates[index]] + [entry])
                index += 1
    
    def Create_PriceDiff_CSV(self, dictionary):
        """
        Create csv file using a dictionary (Normalised Prices)
        """
        with open('price_difference_normalised.csv', 'w', encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Date"] + ["Price (Normalised)"])
            for key in dictionary:
                writer.writerow([key] + [dictionary[key]])
    
    def Create_Headlines_CSV(self, dictionary):
        """
        Create csv file using a dictionary (Headlines)
        """
        with open('test.csv', 'w', encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Date"] + ["Headline"])
            for key in dictionary:
                if(dictionary[key] != 'empty'):
                    writer.writerow([key] + [dictionary[key]])