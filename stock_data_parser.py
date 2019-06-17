from __future__ import division
import csv

class Stock_Data_Object:
    """
    Data object 
    """
    # Memeber variables
    stock_dates = []
    
    stock_open_close = []
    price_diff_normalised = {}

    prices = []
    
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

    def Normalise_Open_Close_Values(self):
        """
        Normalise values to a range between -1,1 
        """
        max_value = max(self.stock_open_close)
        min_value = min(self.stock_open_close)
        index = 0 # Track index of stock_open_close value to use
        for date in self.stock_dates:
            normalised_value = (2 * ((self.stock_open_close[index] - min_value) / (max_value - min_value)) - 1)
            self.prices.append(normalised_value)
            self.price_diff_normalised[date] = normalised_value
            index += 1
        
    def Get_DateColumn(self):
        """
        Returns coloumn with dates for each stock item
        """
        print("Length of stock_dates: %d" % len(self.stock_dates)) 
        return self.stock_dates
    
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
        with open('headlines.csv', 'w', encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Date"] + ["Headline"])
            for key in dictionary:
                writer.writerow([key] + [dictionary[key]])
    
    def PrintTestData(self):
        print(max(self.prices))
        print(min(self.prices))

# Create stock object
stockObject = Stock_Data_Object('fb-stock-history')
stockObject.Normalise_Open_Close_Values()
stockObject.Create_PriceDiff_CSV(stockObject.price_diff_normalised)