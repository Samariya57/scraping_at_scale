# import libraries
import urllib2
from bs4 import BeautifulSoup

DEBUG=True

def main():
    '''
    Function for getting next url in a Queue, retrieve, parse, and store to the DB
    return:
    rtype:
    '''
    # get next combination (or subpage) from the DB
    current_url = "https://www.yelp.com/search?find_desc=thai&find_loc=New+York+10010&start=0&cflt=chinese"
    if DEBUG:
        print current_url
    # get content of the current webpage
    current_page = urllib2.urlopen(current_url)
    if DEBUG:
        print page.read()
    parsed_page = BeautifulSoup(current_page, "html.parser")
    if DEBUG:
        print parsed_page


if __name__ == '__main__':
   main()
