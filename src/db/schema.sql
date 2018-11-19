/* Drop allconnections except current*/

SELECT pg_terminate_backend(pg_stat_activity.pid)
FROM pg_stat_activity
WHERE pg_stat_activity.datname = 'yelp'
  AND pid <> pg_backend_pid();

/* Clean Database */
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;

/* Create a table for all possible combinations of zipcode and category */
CREATE TABLE combinations (
  CombinationID SERIAL,
  Zipcode VARCHAR(15) NOT NULL,
  Category VARCHAR(25) NOT NULL,
  City VARCHAR(25) NOT NULL
);

/* Create a table for all restaurants */
CREATE TABLE restaurants (
  Name VARCHAR(255) NOT NULL,
  Address TEXT NOT NULL,
  Added TIMESTAMP NOT NULL
);

/* Create a table for queue or URLs*/
CREATE TABLE queue (
  Zipcode VARCHAR(15) NOT NULL,
  City VARCHAR(15) NOT NULL,
  Category VARCHAR(25) NOT NULL,
  NumberPerPage INTEGER NULL,
  TotalNumber INTEGER NULL,
  Processed INTEGER NULL,
  LastProcessed TIMESTAMP NULL
);

/* Create a table for IP tracker */
CREATE TABLE ips (
  IPID VARCHAR(25) NOT NULL,
  Scrapped TIMESTAMP NOT NULL,
  Count INTEGER
);

/* Grant permissions for the group of scrapers */
GRANT ALL ON SCHEMA public TO GROUP Scrapers;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO GROUP Scrapers;
