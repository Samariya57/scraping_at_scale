# import libraries
import urllib2
import datetime
import psycopg2
import os
import requests
import random
from time import sleep
from bs4 import BeautifulSoup

def get_connection():
    '''
    Function to get connection to the DB
    '''
    HOST=os.environ['HOST']
    PASSWORD=os.environ['PGPASSWORD']
    configs = "host="+HOST+" port='5432' dbname=yelp user=airflow password="+PASSWORD
    try:
        conn = psycopg2.connect(configs)
    except:
        print "Coudn't connect to the DB"
    return conn


def get_number_of_restaurants(category, city, zipcode):
    '''
    Function for getting number of restaurants per request and total number of
    restaurants for the combination of zipcode and restaurant type
    arguments: type of restaurant and Zipcode
    return: number restaurants per page, total number and date
    '''
    current_url = "https://www.yelp.com/search?find_desc="+category+"&find_loc="+city.replace(" ","+")+"+"+zipcode
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
    response = requests.get(current_url, headers=headers, verify=False).text
    parsed_page = BeautifulSoup(response, "html.parser")
    try:
        showing = [x.find('p') for x in parsed_page.findAll('div') if (x.find('h1') and x.find('p'))]
        # Get number of restaurants for current criteria
        total_number = int(showing[0].text.strip().split()[-1])
        number_per_page = int(showing[0].text.strip().split()[1].split("-")[-1])
        return (number_per_page, total_number)
    except:
        return parsed_page.find('h2').text.replace("\u2019","'").strip()

def get_next_combination():
    '''
    Function to get next uncounted combination of zipcode and category
    rtype: (category, city, zipcode)
    '''
    try:
        conn = get_connection()
        cur = conn.cursor()
        next_combo = "SELECT * FROM queue WHERE Processed is NULL LIMIT 1;"
        cur.execute(next_combo)
        result = cur.fetchone()
        return (result[2], result[1], result[0])
    except:
        print "Can't fetch data"
    finally:
        cur.close()
        conn.close()

def insert_numbers(City, Zipcode, Category, NumberPerPage, TotalNumber, Processed):
    '''
    Function to insert numbers for zipcode and category combination
    '''
    try:
        conn = get_connection()
        cur = conn.cursor()
        sql_in_queue = "INSERT INTO queue (City, Zipcode, Category, NumberPerPage, TotalNumber, Processed) VALUES (%s, %s, %s, %s, %s, %s);"
        cur.execute(sql_in_queue, (City, Zipcode, Category, NumberPerPage, TotalNumber, Processed))
        conn.commit()
    except:
        print "can't insert numbers"
    finally:
        cur.close()
        conn.close()

def main():
    '''
    Function for getting number of restaurants per request and total number of
    restaurants for all possible combinations
    return:
    '''
    current_numbers = (1,1)
    while (current_numbers[1] > 0):
        try:
            combo = get_next_combination()
            current_numbers = get_number_of_restaurants(combo[0], combo[1], combo[2])
            insert_numbers (conbo[1], combo[2], combo[0], current_numbers[0], current_numbers[1],0)
            sleep(random.randint(30, 60))
        except:
            if current_numbers=="Oops, we can't find your location":
                current_numbers = (1,1)
                continue
            elif current_numbers=="Sorry, you’re not allowed to access this page.":
                break
        finally:
            print current_numbers
    return 1

if __name__ == '__main__':
   main()
