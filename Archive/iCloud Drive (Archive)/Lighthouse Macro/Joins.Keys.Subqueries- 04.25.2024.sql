-- Joins, Keys, and Subqueiries lesson on April 25, 2024
SELECT * FROM category 
WHERE name = 'Action'
LIMIT 5;

SELECT * FROM film_category 
WHERE category_id=1;

SELECT film.title, film.length
FROM film JOIN
(SELECT film_category.film_id
FROM category JOIN film_category
ON category.category_id = film_category.category_id
WHERE category.name = 'ACTION') as actionFilms
ON film.film_id = actionFilms.film_id;


SELECT country.country, city_sub.city
FROM  country
JOIN 
(SELECT * FROM city
WHERE city.city = 'Moscow') as city_sub
ON country.country_id = city_sub.country_id;

SELECT country.country, city.city
FROM  country
JOIN city
ON country.country_id = city.country_id
WHERE city.city ='Moscow'; -- less efficient than the above but same result


SELECT staff_id, count(*)
FROM rental
WHERE staff_id = 1
GROUP BY staff_id;


############## JOINS & SUBQUERIES BREAKOUT ROOMS QUESTIONS #############

#1 
-- Show the first and last names and IDs of the customers within the payment table.
SELECT DISTINCT c.customer_id,c.first_name, c.last_name
FROM customer c
JOIN payment p
ON c.customer_id = p.customer_id;

#2 
-- What is the sum of all the payment amounts and the averager payment per customer, including the customer's name?
SELECT c.customer_id AS id, c.first_name, c.last_name, avg(p.amount) as AvgAmt, sum(p.amount) as TotAmt
FROM customer c
JOIN payment p
ON c.customer_id = p.customer_id
GROUP BY id;

#3 List the 5 Customers who have paid the highest amount
SELECT c.customer_id AS id, c.first_name, c.last_name, avg(p.amount) as AvgAmt, sum(p.amount) as TotAmt
FROM customer c
JOIN payment p
ON c.customer_id = p.customer_id
GROUP BY id
ORDER BY TotAmt DESC
LIMIT 5;

#4  What is the name of the actor that has appeared in the most films?
SELECT a.actor_id, a.first_name, a.last_name, COUNT(f.actor_id) as counting
FROM actor a
JOIN film_actor f
ON a.actor_id = f.actor_id
GROUP BY f.actor_id
ORDER BY counting DESC
LIMIT 1;

#5 Extract the details of the films where Morgan and Christian have acted. Find all
SELECT f.fim_id, f.title, f.description
FROM film f
(SELECT a.actor_id, first_name, a.last_name, fa.film_id 
FROM actor a
JOIN film_actor fa
ON a.actor_id = fa.actor_id
WHERE a.first_name = 'Morgan' OR a.first_name = 'Christian') as actors_names
JOIN actors_names an
ON fa.film_id = f.film_id;


#6 Create a list of films and their corresponding categories sorted by film title in ascedining alphabetical order.
SELECT f.title, FCN.catName
FROM film as f
JOIN
(SELECT  fc.film_id, c.name as catName
FROM film_category as fc
JOIN category as c
ON fc.category_id = c.category_id) as FCN
ON f.film_id = FCN.film_id
ORDER BY title ASC;

