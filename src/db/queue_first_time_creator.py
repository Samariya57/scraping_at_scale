# import libraries
import urllib2
import datetime
import psycopg2
import os
import csv

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

def add_to_queue(combinations):
    '''
    Function to write all new restaurants to the database
    '''
    try:
        conn = get_connection()
        cur = conn.cursor()
        joined_combos = ','.join(cur.mogrify("(%s,%s,%s)", combo) for combo in combinations)
        cur.execute("INSERT INTO queue (City, Zipcode, Category) VALUES " + joined_combos)
        conn.commit()
    except:
        print "Can't insert in the db"
    finally:
        cur.close()
        conn.close()


def main():
    with open("ny_zipcodes.csv") as zipfile:
        zipreader = csv.reader(zipfile, delimiter=",")
        for zipcode in zipreader:
            combinations = []
            with open('categories.csv') as categoryfile:
                catreader = csv.reader(categoryfile, delimiter=",")
                for category in catreader:
                    combinations.append((" ".join(zipcode[1].split()[0:-1]),zipcode[0],category[-1]))
                add_to_queue(combinations)



if __name__ == '__main__':
   main()
