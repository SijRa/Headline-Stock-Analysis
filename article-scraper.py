import datetime
from datetime import timedelta
from urllib.request import urlopen as urlRequest
from bs4 import BeautifulSoup as soup
from stock_data_parser import Stock_Data_Object
import time
import string

# All collected headlines
Date_Headline = []

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

def Match_Percentage(matches,limit):
    """
    Calculates match percentage
    """
    return float(matches/limit)

def Check_Match(headline_one,headline_two):
    """
    Returns match percentage between two headlines
    """
    headline_one_word_array = headline_one.split(' ')
    headline_two_word_array = headline_two.split(' ')
    matches = 0
    for word in headline_one_word_array:
        thisWord = word.translate(str.maketrans('', '', string.punctuation))
        for word in headline_two_word_array:
            if(thisWord == word.translate(str.maketrans('', '', string.punctuation))):
                matches += 1
    return Match_Percentage(matches, len(headline_two_word_array))

# Extract headlines from page from source (Reuter)
def Get_Headline(htmlPage):
    """
    Extract headlines
    """
    div_content = []
    duplicate_list = []
    # Top story
    story_div = htmlPage.find('div', {'class':'topStory'})
    if(story_div is not None):
        text = story_div.h2.a.get_text()
        if('UPDATE' not in text):
            div_content.append(story_div.h2.a.get_text())
    # Feature div
    feature_div = htmlPage.find_all('div', {'class':'feature'})
    if(feature_div is not None):
        for section in feature_div:
            text = section.h2.a.get_text()
            if('UPDATE' not in text):
                div_content.append(text)
    if(div_content is None):
        return "empty"
    ordered_headlines = sorted(div_content,key=len)
    # Limit similarity to percentage
    similarity_limit = 0.8
    # Compare headlines
    index_A = 0
    index_B = 1
    while(index_A < len(ordered_headlines) - 1):
        match_percentage = Check_Match(ordered_headlines[index_A],ordered_headlines[index_B])
        if(match_percentage > similarity_limit):
            duplicate_list.append(ordered_headlines[index_B])
        index_A += 1
        index_B += 1
    # Remove duplicates
    for headline in ordered_headlines:
        if(headline in duplicate_list):
            ordered_headlines.remove(headline)
    return ordered_headlines

def Get_Headline_Specific_Date(date):
    """
    Get headlines from a specific date
    """
    date_url = Date_Url_String(date)
    page = Get_Page_Soup(URLS[stock_ticker] + date_url)
    headlines = Get_Headline(page)
    if(headlines is not None):
        Append_Headlines(date,headlines)

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
        headlines = Get_Headline(page)
        if(headlines is not None):
            Append_Headlines(date,headlines)
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

def Append_Headlines(date, headlines):
    """
    Appends key/value pair to headlines dictionary
    """
    for headline in headlines:
        Date_Headline.append([date,headline])
        print(str(date) + " - " + str(headline))

# Choose stock
stock_ticker = "FB"

# Create stock object
stockObject = Stock_Data_Object(stock_ticker)

# Get stock history dates
article_dates = stockObject.Get_DateColumn()

# Start collection
Start_Headline_Collection(article_dates)
stockObject.Create_Headlines_CSV(Date_Headline)
