### Question 1 ###
SELECT *
FROM flights;
/* Ran this query to help familiarize myself with the flights table. */

SELECT * 
FROM airports;
/* Similar to the above, ran this query to quickly familiarize myself with the airports table. */


SELECT COUNT(id)
FROM flights;
/* Total number of flights for both years is 6,521,361. */

-- Subquestion 1. 
-- How many flights were there in 2018 and 2019 seperately?
-- 2018
SELECT COUNT(id)
FROM flights
WHERE flightdate LIKE '%2018%';
/* Total number of flights in 2018 is 3,218,653 */

-- 2019
SELECT COUNT(id)
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
WHERE Cancelled = 1
GROUP BY CancellationReason;
/* Weather - 50,225 flights cancelled
Carrier - 34,141 flights cancelled
National Air Security - 7,962 flights cancelled
Security - 35 flights cancelled */

-- Subquestion 4. 
-- For each month in 2019, report both the total both the total number of flights and percentage of flights cancelled.
-- Based on your results, what might you say about the cyclic nature of the airline revenue?
SELECT MONTH(flightdate) AS Month,COUNT(*) AS FlightsPerMonth,
	(SUM(CASE WHEN cancelled = 1 THEN 1 ELSE 0 END) / COUNT(*)) * 100 AS PctCancelled
FROM flights
WHERE YEAR(flightdate) = 2019
GROUP BY MONTH(flightdate)
ORDER BY Month;
/* Based on the data, there are less cancelled flights around the end of the year, particularly the holiday season in November and December.
Thus, we can see the cyclicality of the industry wherein Q4 is the time of year when airlines have the least lost revenue due to flight cancellations.
Additionally, one could deteremine that winter and early spring results in the most cancellations. Given our results in subqeustion 3, 
one could likely assume the greater cancellations during Q1 is largely a result of poorer weather. */




### Question 2 ###
-- 1. Create two new tables, one for each year (2018 and 2019) showing the total miles traveled and number of flights broken down by airline.
-- Table for 2018
CREATE TABLE airline_stats_2018 AS
SELECT AirlineName, SUM(distance) AS total_miles, COUNT(*) AS num_flights
FROM flights
WHERE YEAR(flightdate) = 2018
GROUP BY airlinename;

SELECT * FROM airline_stats_2018;

-- Table for 2019
CREATE TABLE airline_stats_2019 AS
SELECT AirlineName, SUM(distance) AS total_miles, COUNT(*) AS Num_flights
FROM flights
WHERE YEAR(flightdate) = 2019
GROUP BY airlinename;

SELECT * FROM airline_stats_2019;
/*two tables have been created breaking down the airline statistics for each year, 2018 and 2019 respectively. */

-- 2. Using you new tables, find the year-over-year percent change in total flights and miles traveled for each airline.
SELECT a.AirlineName, a.num_flights AS total_flights_2018, b.num_flights AS total_flights_2019,
    CASE
        WHEN a.num_flights = 0 THEN NULL
        ELSE ((b.num_flights - a.num_flights) / a.num_flights) * 100
    END AS flights_percent_change,
    a.total_miles AS total_miles_2018,
    b.total_miles AS total_miles_2019,
    CASE
        WHEN a.total_miles = 0 THEN NULL
        ELSE ((b.total_miles - a.total_miles) / a.total_miles) * 100
    END AS miles_percent_change
FROM airline_stats_2018 a
JOIN airline_stats_2019 b ON a.AirlineName = b.AirlineName
ORDER BY a.AirlineName;
-- What investment guidance would you give to the fund managers based on your results?

/* My investment guidance would be to focus on Delta Air Lines, as Delta showed the greatest improvement year-over-year for both in total flights percentage change
 and in total miles traveled percentage chane with ~4.5% and 5.56% respectively. This compares to more meager growth from American Airlines of only 3.26% and 0.56% respectively.
 Southwest Airlines struggled the most with only 0.84% increase in flights y/y and actually seeing a decline of -0.12% in miles y/y.
 While further due diligence is likely needed before committing funds, this analysis bodes well for Delta's growth prospects
 and shows them to be clearly ahead of it's competitors with respect to gaining flight & mile market share. */


### Question 3 ###
-- Another critical piece of information is what airports the three airlines utilize most commonly.
-- 1. What are the names of the 10 most popular destination airports overall? 
-- For this question, generate a SQL query that first joins flights and airports then does the necessary aggregation.
SELECT a.AirportID, a.AirportName AS AirportName, COUNT(*) AS total_arrivals
FROM flights f
JOIN airports a ON f.DestAirportID = a.AirportID
GROUP BY f.DestAirportID, a.AirportName
ORDER BY total_arrivals DESC
LIMIT 10;
        
-- 2. Answer the same question but using a subquery to aggregate & limit the flight data before your join with the airport information, hence optimizing your query runtime.
SELECT a.AirportID, a.AirportName AS AirportName, f.total_arrivals
FROM (SELECT DestAirportID, COUNT(*) AS total_arrivals
	  FROM flights
	  GROUP BY DestAirportID
	  ORDER BY total_arrivals DESC
	  LIMIT 10) f
JOIN airports a ON f.DestAirportID = a.AirportID;

/* The first query has a signficantly longer runtime.
1st Query ~12.6 seconds 
2nd Query ~1.7 seconds. 
This is because using a subquery helps to make the overall query more efficient, thus resulting in a faster run time. */




### Question 4 ###
-- The fund managers are interested in operating costs for each airline..
-- As such, each plane has a unique tail number and the number of unique tail numbers for each airline should approximate how many planes the airline operates in total. 
-- Subquestion 1. Using this information, determine the number of unique aircrafts each airline operated in total over 2018-2019.
SELECT AirlineName, COUNT(DISTINCT Tail_Number) AS Unique_Aircrafts
FROM flights
Group BY AirlineName;
/* American Airlines - 993 Unique Aircraft
Delta Air Lines - 988 Unique Aircraft 
Southwest Airlines - 754 Unique Aircraft */
        

-- Similarly, the total miles traveled by each airline gives an idea of total fuel costs and the distance traveled per plane gives an approximation of total equipment costs. 
-- Subquestion 2.  What is the average distance traveled per aircraft for each of the three airlines?
SELECT AirlineName, COUNT(DISTINCT Tail_Number) AS Unique_Aircrafts, SUM(Distance) AS Total_Distance,
        SUM(Distance)/COUNT(DISTINCT Tail_Number) AS Avg_Distance_Per_Aircraft
From flights
GROUP BY AirlineName;

-- Compare the three airlines with respect to your findings: how do these results impact your estimates of each airline's finances? 
/* American Arilines - Total Distance 1,871,422,719 & Avg Per Airracft 1,884,615
Delta - Total Distance 1,731,686,703 & Avg Per Aircraft 1,752,719
Southwest - Total Distance 2,024,430,929 & Avg Per Aircraft 2,684,921
We can see that Delta traveled the least amount amount of total miles likely leading to the lowest fuel cost of the group. 
Additionally, they had the lowest average distance per aircraft likely keeping equipment costs down. In continuing with what was discussed above, 
Delta not only seems to be growing the fastest of the 3 airlines, it also seems to be keeping it's costs down thru
lower fuel usage and less wear & tear on their fleet of aircrafts. */



### Question 5 ###
-- Subquestion 1. Find the average departure delay for each time-of-day across the whole data set. Can you explain the pattern you see?
SELECT Avg(DepDelay),
	CASE
		WHEN HOUR(CRSDepTime) BETWEEN 7 AND 11 THEN "1-morning"
		WHEN HOUR(CRSDepTime) BETWEEN 12 AND 16 THEN "2-afternoon"
		WHEN HOUR(CRSDepTime) BETWEEN 17 AND 21 THEN "3-evening"
		ELSE "4-night"
	END AS "time_of_day"
FROM flights 
GROUP BY time_of_day
ORDER BY AVG(DepDelay) DESC;
    
/* The greatest delays happen in evening followed by the afternoon. 
These time periods are likely the busiest times for flights/airport traffic which likely accounts for the larger delay times. */

-- Subquestion 2 Now, find the average departure delay for each airport and time-of-day combination.
SELECT Avg(DepDelay), OriginAirportID,
	CASE
		WHEN HOUR(CRSDepTime) BETWEEN 7 AND 11 THEN "1-morning"
		WHEN HOUR(CRSDepTime) BETWEEN 12 AND 16 THEN "2-afternoon"
		WHEN HOUR(CRSDepTime) BETWEEN 17 AND 21 THEN "3-evening"
		ELSE "4-night"
	END AS "time_of_day"
FROM flights 
GROUP BY OriginAirportID, time_of_day
ORDER BY AVG(DepDelay) DESC;

/* While the query does show us the intended info based on the questions,
the highest results are much smaller airports with less flights that have very large average departure days being at the top.
For example, AirportID 14457, which is Rapid City Regional in Rapid City, SD has the highest average departure delay in the 
afternoon with an avg delay time of 307min. The next query and explanation will help to make the data a bit more usable. */

-- Subquestion 3 Next, limit your average departure delay analysis to morning delays and airports with at least 10,000 flights.

SELECT Avg(DepDelay), OriginAirportID
FROM flights 
WHERE HOUR(CRSDepTime) Between 7 AND 11
	  AND OriginAirportID IN 
			(SELECT OriginAirportID
             FROM flights
             GROUP BY OriginAirportID
             HAVING COUNT(*) >= 10000)
GROUP BY OriginAirportID
ORDER BY AVG(DepDelay) DESC;

/*  This query helps to normalize the above and what I had discussed in my answer underneath. The smaller regional airports with 
less flights are filtered out to give us more usable data points that are more in-line with what we can
expect on the whole. */

-- Subquestion 4 
SELECT a.airportid, a.city, a.AirportName, AVG(f.DepDelay) as Avg_Morning_Dep_Delay
FROM airports a
JOIN
    (SELECT OriginAirportID, AVG(DepDelay) as DepDelay
	 FROM flights
	 WHERE HOUR(CRSDepTime) BETWEEN 7 AND 11
	 GROUP BY OriginAirportID
	 HAVING COUNT(*) >= 10000) f ON a.AirportID = f.OriginAirportID
GROUP BY a.AirportID, a.City, a.AirportName
ORDER BY Avg_Morning_Dep_Delay DESC
LIMIT 10;

/* The 10 airports with the largest average morning departure delay times are
1. San Francisco International
2. Los Angeles International
3. Dallas/Fort Worth International
4. Chicago O'Hare
5. Chicago Midway
6. Seattle/Tacoma International
7. Denver International
8. Dallas Love Field
9.  William P Hobby (located in Houston)
10. San Diego International 
 We can see these international airports in large hub cities which tend to have a larger amount of flights
 and logistical considerations, which would likely lead to persistent delays during peak hours. */




