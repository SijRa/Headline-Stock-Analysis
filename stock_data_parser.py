import csv


class Stock_Data_Object:
    """
    Data object 
    """
    # Memeber variables
    stock_dates = []
    fileName = ""

    # Constructor
    def __init__(self, fileName):
        self.fileName = fileName 
        with open(fileName + '.csv', 'r') as csvfile:
            rawData = csv.reader(csvfile, delimiter=',', quotechar=',')
            # Read data
            for row in rawData:
                if(row[0] == 'Date'):
                    continue
                self.stock_dates.append(row[0]) # Dates

    def Get_DateColumn(self):
        """
        Returns coloumn with dates for each stock item
        """
        print("Length of stock_dates: %d" % len(self.stock_dates)) 
        return self.stock_dates
    
    def Create_CSV(self, dictionary):
        """
        Create csv file using a dictionary
        """
        with open('headlines_2.csv', 'w', encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Date"] + ["Headline"])
            for key in dictionary:
                writer.writerow([key] + [dictionary[key]])