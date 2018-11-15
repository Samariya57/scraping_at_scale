/* Clean Database */
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;

/* Create a table for all possible combinations of zipcode and category */
CREATE TABLE combinations (
  CombinationID SERIAL,
  Zipcode VARCHAR(15) NOT NULL,
  Category VARCHAR(25) NOT NULL
);

/* Create a table for all restaurants */
CREATE TABLE restaurants (
  RestaurantID TEXT NOT NULL,
  Address TEXT NOT NULL,
  Name VARCHAR(255) NOT NULL,
  Added TIMESTAMP NOT NULL
);

/* Create a table for queue or URLs*/
CREATE TABLE queue (
  Zipcode VARCHAR(15) NOT NULL,
  Category VARCHAR(25) NOT NULL,
  NumberPerPage INTEGER NULL,
  TotalNumber INTEGER NULL,
  Added TIMESTAMP NOT NULL,
  Scrapped BOOLEAN NOT NULL
);

/* Create a table for IP tracker */
CREATE TABLE ips (
  IPID VARCHAR(25) NOT NULL,
  Scrapped TIMESTAMP NOT NULL,
  Count INTEGER
);
