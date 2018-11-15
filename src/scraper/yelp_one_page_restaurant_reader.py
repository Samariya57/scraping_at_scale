# import libraries
import urllib2
import datetime
import psycopg2
from bs4 import BeautifulSoup


def get_all_restaurants_from_one_page(current_url):
    '''
    Fucntion to parce info about restaurants from the webpage
    arguments: url
    return: list of restaurants info
    rtype: [(restaurant_name, restaurant_address)]
    '''
    current_page = urllib2.urlopen(current_url)
    parsed_page = BeautifulSoup(current_page, "html.parser")
    restaurants = parsed_page.findAll('li', attrs={'class': 'regular-search-result'})
    # Get name and address of all restaurnts from the current page and store them in a list
    # Also, clean unpritable characters
    results = []
    for venue in restaurants:
        current_name = venue.find('a', attrs={'class': 'biz-name js-analytics-click'}).find('span').text.replace(u"\u2019", "'").strip()
        current_address = venue.find('address').text.replace(u"\u2019", "'").strip()
        results.append((current_name,current_address))
    return results

def main():
    '''
    Function for getting next url in a Queue, retrieve, parse, and store to the DB
    '''
    # get next combination (or subpage) from the DB
    current_url = "https://www.yelp.com/search?find_desc=thai&find_loc=New+York+10010&start=0&cflt=chinese"

    restaurants = parsed_page.findAll('li', attrs={'class': 'regular-search-result'})
    for venue in restaurants:
        current_name = venue.find('a', attrs={'class': 'biz-name js-analytics-click'}).find('span').text.replace(u"\u2019", "'").strip()
        current_address = venue.find('address').text.replace(u"\u2019", "'").strip()
    today = datetime.datetime.today().strftime('%Y-%m-%d')




if __name__ == '__main__':
   main()
