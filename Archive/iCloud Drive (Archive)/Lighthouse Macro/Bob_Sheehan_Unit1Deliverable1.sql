### Question 1 ###
SELECT *
FROM flights;

SELECT COUNT(id)
FROM flights;
/* Total number of flights for both years is 6,521,361. */

-- Subquestion 1. 
-- How many flights were there in 2018 and 2019 seperately?
-- 2018
SELECT count(id)
FROM flights
WHERE flightdate LIKE '%2018%';
/* Total number of flights in 2018 is 3,218,653 */

-- 2019
SELECT count(id)
FROM flights
WHERE flightdate LIKE '%2019%';
/* Total number of flights in 2019 is 3,302,708 */

-- Subquestion 2. 
-- In total, how many flights were cancelled or departed late over both years?
SELECT count(id)
FROM flights 
WHERE DepDelay > 0 OR Cancelled = 1;
/* Total number of flights that were cancelled or departed late over both years is 2,633,237 */

-- Subquestion 3. 
-- Show the number of flights that were cancelled broken down by the reason.
SELECT count(id)
FROM flights
WHERE cancelled = 1;
/* Total number of flights cancelled is 92,363. Will break down by cancellation reason in query below. */

SELECT count(id), cancellationreason
FROM flights
WHERE Cancelled = 1f
GROUP BY CancellationReason;
/* Weather - 50,225 flights cancelled
Carrier - 34,141 flights cancelled
National Air Security - 7,962 flights cancelled
Security - 35 flights cancelled */

-- Subquestion 4. 
-- For each month in 2019, report both the total both the total number of flights and percentage of flights cancelled.
-- Based on your results, what might you say about the cyclic nature of the airline revenue?
SELECT count(id) as TotalCount 
FROM    flights
WHERE   flightdate >= '2019-01-01'
AND     flightdate <= '2019-12-31'
GROUP BY format(flightdate,'MM');



### Question 2 ###
-- 1. Create two new tables, one for each year (2018 and 2019) showing the total miles traveled and number of flights broken down by airline.
-- 2. Using you new tables, find the year-over-year percent change in total flights and miles traveled for each airline.
-- Use fully commented SQL queries to address the questions above.
-- What investment guidance would you give to the fund managers based on your results?


### Question 3 ###
-- Another critical piece of information is what airports the three airlines utilize most commonly.
-- 1. What are the names of the 10 most popular destination airports overall? 
		-- For this question, generate a SQL query that first joins flights and airports then does the necessary aggregation.
-- 2. Answer the same question but using a subquery to aggregate & limit the flight data before your join with the airport information, hence optimizing your query runtime.
-- If done correctly, the results of these two queries are the same, but their runtime is not. In your SQL script, comment on the runtime: which is faster and why?

