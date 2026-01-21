-- Campaigns
SELECT * FROM campaign LIMIT 10;

SELECT COUNT(*) FROM campaign;

SELECT  name, outcome, backers, pledged
FROM campaign
WHERE backers >= 500;

SELECT  name, outcome, backers
FROM campaign
WHERE (pledged > 20000) AND (country_id = 1);

SELECT DISTINCT outcome FROM campaign;

SELECT name, pledged
FROM campaign
WHERE outcome = 'successful'
LIMIT 10;

SELECT name, pledged 
FROM campaign
WHERE NOT (outcome = 'failed')
      AND (backers > 500 OR pledged > 5000);

SELECT *
FROM campaign
ORDER BY backers 
LIMIT 15;

-- We will now use the sakila database
SET GLOBAL sql_mode = 'ONLY_FULL_GROUP_BY'; 
SELECT count(*) FROM actor; -- this it the number of actors

SELECT count(actor_id) from actor; -- same thing as above

SELECT language_id, COUNT(*), AVG(length) AS avglen
FROM film
WHERE length > 10
GROUP BY language_id;

SELECT rating, release_year,  AVG(replacement_cost), AVG(length)
FROM film
GROUP BY rating, release_year
ORDER BY release_year DESC, rating ASC;

SELECT rating, COUNT(rating) as numMovies, avg(length)
FROM film
WHERE NOT rating = 'PG' -- happens before the grouping
GROUP BY rating
HAVING avg(length)>112; -- happens after the grouping


-- results will be different from following query
SELECT rating, COUNT(rating) as numMovies, avg(length)
FROM film
GROUP BY rating;

SELECT rating, COUNT(rating) as numMovies, avg(length)
FROM film
WHERE length > 112
GROUP BY rating;

SELECT * FROM film LIMIT 10;


SELECT title, length/rental_rate as Length_per_rate, length, rental_rate
FROM film
LIMIT 10;


## next 4 queries from breakout groups on slide 40 
#1
SELECT name
FROM language
ORDER BY name ASC;

#2
SELECT COUNT(*) FROM film
WHERE length > 180;

#3
SELECT AVG(amount) AS Average,  MAX(amount) AS Maximum, MIN(amount) as Minimum
FROM payment;

#4
SELECT COUNT(rental_id)
FROM rental
WHERE customer_id = 26 AND staff_id = 2;


## next 4 queries from breeakout group on slide 48
#1
SELECT staff_id, avg(amount)
FROM payment
GROUP BY staff_id;

#2

