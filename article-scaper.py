import datetime
from datetime import timedelta
from urllib.request import urlopen as urlRequest
from bs4 import BeautifulSoup as soup
from stock_data_parser import Stock_Data_Object
import time

# All collected headlines
Date_Headline_Dict = {}

# Reuter FAANG URLS
URLS = {
    'FB':'https://www.reuters.com/finance/stocks/company-news/FB.OQ',
    'APPL':'https://www.reuters.com/finance/stocks/company-news/AAPL.OQ',
    'AMZN':'https://www.reuters.com/finance/stocks/company-news/AMZN.OQ',
    'NFLX':'https://www.reuters.com/finance/stocks/overview/NFLX.OQ',
    'GOOG':'https://www.reuters.com/finance/stocks/company-news/GOOG.OQ'
}

def Convert_Date_To_Weekday(dt):
    """
    Convert date to weekday: 0-6 Monday-Sunday
    """
    year = int(dt.split('-')[0])
    month = int(dt.split('-')[1])
    day = int(dt.split('-')[2])
    return datetime.datetime(year, month, day).weekday()

# New date url -- MM/DD/YYYY
def Date_Url_String(date):
    """
    Date input format YYYY-MM-DD converted to url string for Reuter url
    """
    year = date.split('-')[0]
    month = date.split('-')[1]
    day = date.split('-')[2]
    return '?' + 'date=' + month + day + year 

# Open html page
def Get_Page_Soup(url):
    """
    Download html page source
    """
    uClient = urlRequest(url)
    page_html = uClient.read()
    uClient.close()
    page_soup = soup(page_html, "html.parser")
    return page_soup

# Extract top story from page from source (reuter)
def Get_Headline(htmlPage):
    """
    Extract headline
    """
    storyDiv = htmlPage.find('div', {'class':'feature'})
    if storyDiv is None:
        storyDiv = htmlPage.find('div', {'class':'topStory'})
    if storyDiv is not None:
        text = storyDiv.h2.a.get_text()
        return text
    else:
        return "empty"

def Get_Headline_Specific_Date(date):
    """
    Get headline from a specific date
    """
    date_url = Date_Url_String(date)
    page = Get_Page_Soup(URLS[stock_ticker] + date_url)
    story_headline = Get_Headline(page)
    Add_To_Headlines_Dict(date,story_headline)
    print(date + " : " + story_headline)

def Check_Weekend_Headlines(date, last_date):
    """
    Extracts headlines for the weekend 
    """
    if(date != last_date):
        if(Convert_Date_To_Weekday(date) == 4):
            Collect_Weekend_Headlines(date)


def Start_Headline_Collection(date_list):
    """
    Collect headlines from a set of dates
    """
    url = URLS[stock_ticker]
    for date in date_list:
        date_url = Date_Url_String(date)
        page = Get_Page_Soup(url + date_url)
        story_headline = Get_Headline(page)
        Add_To_Headlines_Dict(date,story_headline)
        print(date + " : " + story_headline)
        time.sleep(1) # Sleep to avoid blacklist
        Check_Weekend_Headlines(date,date_list[-1])

def Collect_Weekend_Headlines(current_date):
    """
    Collect headlines from the weekend
    """
    weekend = []
    # Add Saturday and Sunday dates
    weekend.append((datetime.datetime.strptime(current_date, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d'))
    weekend.append((datetime.datetime.strptime(current_date, '%Y-%m-%d') + timedelta(days=2)).strftime('%Y-%m-%d'))
    for date in weekend:
        Get_Headline_Specific_Date(date)

def Add_To_Headlines_Dict(date, headline):
    """
    Appends key/value pair to headlines dictionary
    """
    Date_Headline_Dict[date] = headline

# Choose stock
stock_ticker = "FB"

# Create stock object
stockObject = Stock_Data_Object(stock_ticker)
# Get stock history dates
article_dates = stockObject.Get_DateColumn()

# Start collection
Start_Headline_Collection(article_dates)
stockObject.Create_Headlines_CSV(Date_Headline_Dict)