# Scraping at scale
First we have to create a queue with all page that you want to scrape.
Script ```amount_of_work_predictor.py``` is doing exactly that.
And script ```one_page_reader.py``` is reading results for one item from queue.

## Amount of work predictor
Each service search request looks similar to:
~~~
https://www.service.com/search?find_desc=thai&find_loc=zipcode+10010&start=50&cflt=chinese
Where:
  chinese - type of food
  10010 - zipcode of the restaurants
  50 - offset for the search results
~~~

For each combination of Category and Zipcode this script will:
  * get search results
  * get number of restaurants satisfied these criteria
    screenshot to add
  * save this number in the table to understand how many requests for each combination we need

## One request scraper

 And response for each service search request is a web page with k of n restaurants.
 For each restaurant we will save Name and Address, so that within particular zipcode this combination is unique.
