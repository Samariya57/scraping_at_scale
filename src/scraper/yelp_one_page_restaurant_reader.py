# import libraries
import urllib2
import datetime
import psycopg2
from bs4 import BeautifulSoup

def get_connection():
    '''
    Function to get connection to the DB
    '''
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
    current_page = urllib2.urlopen(current_url)
    parsed_page = BeautifulSoup(current_page, "html.parser")
    restaurants2 = parsed_page.findAll('li', attrs={'class': 'regular-search-result'})
    # Get name and address of all restaurnts from the current page and store them in a list
    # Also, clean unpritable characters
    results = []
    for venue in restaurants2:
        current_name = venue.find('div', attrs={'class': 'biz-attributes'}).find('span').text.replace(u"\u2019", "'").strip()
        current_address = venue.find('address').text.replace(u"\u2019", "'").strip()
        results.append((current_name,current_address))
    return results

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
        print count
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
    current_url = "https://www.yelp.com/search?find_desc=food&find_loc=New+York+10027&start=10&cflt=desserts"
    restaurants_from_page = get_all_restaurants_from_one_page(current_url)
    only_new_restaurants = get_only_new_restaurants(restaurants_from_page)
    add_restaurants(only_new_restaurants)









if __name__ == '__main__':
   main()
