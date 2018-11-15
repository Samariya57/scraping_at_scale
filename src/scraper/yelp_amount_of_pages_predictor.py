# import libraries
import urllib2
import datetime
import psycopg2
import os
from bs4 import BeautifulSoup


def get_number_of_restaurants(category, zipcode):
    '''
    Function for getting number of restaurants per request and total number of
    restaurants for the combination of zipcode and restaurant type
    arguments: type of restaurant and Zipcode
    return: number restaurants per page, total number and date
    '''
    current_url = "https://www.yelp.com/search?find_desc="+category+"&find_loc="+zipcode
    current_page = urllib2.urlopen(current_url)
    # Get number of restaurants for current criteria
    total_number = int(parsed_page.find('span', attrs={'class': 'pagination-results-window'}).text.split()[-1])
    number_per_page = int(parsed_page.find('span', attrs={'class': 'pagination-results-window'}).text.split()[1].split("-")[-1])
    return (number_per_page, total_number)

def main():
    '''
    Function for getting number of restaurants per request and total number of
    restaurants for all possible combinations
    return:
    rtype:
    '''
    HOST=os.environ['HOST']
    PASSWORD=os.environ['PGPASSWORD']
    conn = psycopg2.connect("host="+HOST+" port='5432' dbname=yelp user=airflow password="+PASSWORD)
    cur = conn.cursor()
    sql_in_queue = "INSERT INTO queue (Zipcode, Category, NumberPerPage, TotalNumber, Added, Scrapped) VALUES (%s, %s, %s, %s, %s, %s);"
    # get lists of categories and zipcodes
    categories = ['chinese']
    zipcodes = ['10010']
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    # get numbers for all combinations and write them to db
    for category in categories:
        for zipcode in zipcodes:
            current_numbers = get_number_of_restaurants(category, zipcode)
            cur.execute(sql_in_queue, (zipcode, category, current_numbers[0], current_numbers[1], today, False))
    conn.commit()
    cur.close()
    conn.close()


if __name__ == '__main__':
   main()
