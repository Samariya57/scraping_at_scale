# Yelp amount of work predictor

For each combination of Category and Zipcode:
  * get search results
  * get number of restaurants satisfied these criteria
    screenshot to add 
  * save this number in the table to understand how many machines we need

# Yelp one request scraper

Each Yelp search request looks like:
~~~
https://www.yelp.com/search?find_desc=thai&find_loc=zipcode+10010&start=50&cflt=chinese
Where:
  chinese - type of food
  10010 - zipcode of the restaurants
  50 - offset for the search results
~~~
 And response is a web page with k of n restaurants.

 For each restaurant we will save Name and Address, so that within particular zipcode this combination is unique.
