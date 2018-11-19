# import libraries
import urllib2
import datetime
import psycopg2
import requests
import os
import random
from time import sleep
from bs4 import BeautifulSoup

def clean_string(word):
    '''
    Function that replaces some characters and strips text
    '''
    return word.replace(u"\u2019", "'").replace(u"\u2018", "'").replace(u"\u0026","&").strip()

def get_connection():
    '''
    Function to get connection to the DB
    '''
    os.system("source ~/.env")
    HOST=os.environ['HOST']
    PASSWORD=os.environ['PGPASSWORD']
    try:
        conn = psycopg2.connect("host="+HOST+" port='5432' dbname=yelp user=airflow password="+PASSWORD)
    except:
        print "Coudn't connect to the DB"
    return conn


def get_all_restaurants_from_one_page(current_url):
    '''
    Fucntion to parce info about restaurants from the webpage
    arguments: url
    return: list of restaurants info
    rtype: [(restaurant_name, restaurant_address)]
    '''
    #request page with restaurants results
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
    response = requests.get(current_url, headers=headers, verify=False).text
    parsed_page = BeautifulSoup(response, "html.parser")
    #find all listed elements
    current_restaurants = parsed_page.findAll('li')
    #find all names and addresses
    return [(clean_string(x.find('address').text),clean_string(x.find('h3').find('a').text)) for x in current_restaurants if (x.find('address') and (x.find('h3')))]

def get_only_new_restaurants(restaurants):
    '''
    Function to check existance of each restaurant from the input list and return new ones
    input: list of restaurants
    return: list of new restaurants
    rtype: [(Name, Address, Date)]
    '''
    new_restaurants = []
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "prepare myplan as "
        "SELECT COUNT(*) FROM restaurants WHERE Name = $1 AND Address = $2;")
    for restaurant in restaurants:
        cur.execute("execute myplan (%s, %s)", (restaurant[0], restaurant[1]))
        count = int(cur.fetchone()[0])
        if count == 0:
            new_restaurants.append((restaurant[0], restaurant[1], today))
    cur.close()
    conn.close()
    return new_restaurants

def add_restaurants(restaurants):
    '''
    Function to write all new restaurants to the database
    '''
    try:
        conn = get_connection()
        cur = conn.cursor()
        all_restaurants = ','.join(cur.mogrify("(%s,%s,%s)", venue) for venue in restaurants)
        cur.execute("INSERT INTO restaurants VALUES " + all_restaurants)
        conn.commit()
    except:
        print "Can't insert restaurants in the db"
    finally:
        cur.close()
        conn.close()

def main():
    '''
    Function for getting next url in a Queue, retrieve, parse, and store to the DB
    '''
    # get next combination (or subpage) from the DB
    for i in range(5):
        current_url = "https://www.yelp.com/search?find_desc=food&find_loc=New+York+10027&start="+str((i+1)*30)+"&cflt=desserts"
        restaurants_from_page = get_all_restaurants_from_one_page(current_url)
        only_new_restaurants = get_only_new_restaurants(restaurants_from_page)
        if only_new_restaurants:
            add_restaurants(only_new_restaurants)
        sleep(random.randint(30, 60))

if __name__ == '__main__':
   main()
