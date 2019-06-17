from stock_data_parser import Stock_Data_Object




# Create stock object
stockObject = Stock_Data_Object('fb-stock-history')
# Get stock history dates
article_dates = stockObject.Get_DateColumn()