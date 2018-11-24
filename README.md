# How to scrape at scale?

## Why is it hard?
Lots of people are trying to steal data with the help of bots. So services such as Yelp or Zillow are working hard to protect their data from inappropriate usage and creating complicated algorithms to block “spiders”.


## What if I want to try?
You should know that services are tracking activity from each IP and user agents and then block IP (temporary or permanently) if they found any kind of suspicious activity. A couple of years ago I thought that if you do everything slow then I won’t be caught. It’s partially true, but it’s better to be prepared and have a mechanism to rotate your IP and user agents. That being said, you have to follow only 3 steps to get what you need:
* Identify for each webpage what kind of information do you want to scrape
* Create an algorithm to build a queue of pages that you want to scrape
* Get a mechanism to rotate your IPs and user agents

## My approach for ratating mechanism

### Pipeline
![alt text](https://github.com/Samariya57/scraping_at_scale/blob/master/images/pipeline.png "Scraping pipeline")
