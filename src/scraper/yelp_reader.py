# import libraries
#import urllib2
#from bs4 import BeautifulSoup



def main():
    '''

    '''
    # get next combination (or subpage) from the DB
    current_url = "https://www.yelp.com/search?find_desc=thai&find_loc=New+York+10010&start=0&cflt=chinese"
    if DEBUG:
        print current_url
    # get content of the current webpage
    current_page = urllib2.urlopen(current_url)
    if DEBUG:
        print page.read()

if __name__ == '__main__':
   main()
