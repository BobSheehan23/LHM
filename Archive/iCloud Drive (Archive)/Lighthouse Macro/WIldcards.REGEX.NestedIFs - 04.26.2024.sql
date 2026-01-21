DESC campaign;

# The "%" Wildcard helps us to filter for any number of any character 
SELECT * FROM CAMPAIGN
WHERE name LIKE '%pinball%';

## REGEX 

SELECT * 
FROM campaign 
WHERE name REGEXP '^[abc].*[abc]$';


#### NESTED IFs() ####
USE sakila;

SELECT title, rental_rate, length,
IF(length  < 50, 'short', if(length > 120, 'long', 'med')) as long_short
FROM film;


### Case When

SELECT title, rental_rate, length,
CASE
	
    WHEN length < 50 then 'short'
    WHEN length <= 120 then 'regular'
    else 'long'
END  as duration_indicator
FROM film;

SELECT * FROM city
WHERE city LIKE 'ad___';

SELECT *
FROM film_text 
WHERE description
LIKE '%boring%dentist%';

SELECT *
FROM city 
WHERE BINARY city
LIKE 'Ad___';


SELECT 
IF (length >= 50, 'long', 'short') as long_short,
	AVG(length) as avg_length,
    AVG(rental_rate) as avg_rate
FROM film
GROUP BY long_short;

SELECT category_id,
CASE 
WHEN category_id %5=0 AND category_id %3=0 THEN 'FizzBuzz'
WHEN category_id %3=0 then 'Fizz'
WHEN category_id %5=0 then 'Buzz'
ELSE category_id
END
FROM category;



## REGEX problem page 30
USE customer_contacts;

select * from contactdata;

## Pattern to find phone numbers ###
select * from contactdata
WHERE data REGEXP '^\\([09]{3}\\-[0-9]{3}-[0-9]{4}$'