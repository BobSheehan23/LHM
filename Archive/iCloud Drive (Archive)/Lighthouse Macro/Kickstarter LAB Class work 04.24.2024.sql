-- Kickstarter LAB Class work 04/24/2024

#1
-- As a first step let's find the 20 most ambitious campaigns. Which campaigns set the highest funding goals? Which ones set the lowest funding goals?
-- Top 20
SELECT name, goal
FROM campaign
ORDER BY GOAL DESC
LIMIT 20;

-- Bottom 20
SELECT name, goal
FROM campaign
ORDER BY goal ASC
Limit 20;

#2
-- As the last queries showed we can have some issues with our data. 
-- Some values in the table could be entirely unrealistic. 
-- For example, we may consider a Kickstarter campaign with a goal of under $1000.00 to be a typo in the system, or something so low that we don't want to include it in our analysis. 
-- Write a query to find out how many campaigns set a goal under $1000, (you should also check how many set a goal over $1000). Next, write a query to filter out these rows.

SELECT count(goal) AS unrealistic_campaigns
FROM campaign
WHERE goal < 1000 AND currency_id = 2 ;

SELECT name, goal
FROM campaign
WHERE goal > 1000 AND currency_id = 2
ORDER BY goal
LIMIT 20 ;

SELECT name, goal
FROM campaign
WHERE goal > 1000 AND currency_id = 2
ORDER BY goal DESC
LIMIT 20 ;

#3
-- If we define the success of a campaign as how far it exceeded its funding goal,
-- how would you find the most successful campaigns?
-- Does it make a difference if you define success as a ratio or difference?
-- What happens if you exclude campaigns we decided had unrealistic (or possibly incorrect) goals?

SELECT pledged/goal AS success_ratio, name
FROM campaign 
WHERE pledged/goal > 1 AND goal > 1000
ORDER BY success_ratio DESC
LIMIT 20;

#4 
-- Are there any campaigns that were not successful despite the fact they met their funding goal?
-- Can you get a count of the number of campaigns that meet this criteria?
-- Repeat the question but instead of looking at the campaigns that were not successful, look at the campaigns that failed.

SELECT name, goal, pledged, outcome 
FROM campaign
WHERE NOT(outcome = 'successful') and pledged >= goal;

SELECT count(name)
FROM campaign
WHERE NOT(outcome = 'successful') and pledged >= goal;

SELECT name, goal, pledged, outcome 
FROM campaign
WHERE (outcome = 'failed') and pledged >= goal;

#5
-- After digging into the data you may have noticed that the Kickstarter campaigns come from many different countries. 
-- Working with international data is super cool, but in our previous queries, we overlooked the different currencies! 
-- Let's look back at challenge three and focus on the top 10 most successful campaigns by difference.
-- Which currencies are the 10 campaigns using?
-- Let’s assume the campaign goal and pledge amounts are listed in their foreign currency (they are actually pre-converted). 
-- If you convert them all to USD does this change the order?
-- HINT: You will have to manually query the appropriate campaign and currency tables and convert any currencies by looking up the conversion rate online.

SELECT pledged/goal AS success_ratio, name, currency_id
FROM campaign 
WHERE pledged/goal > 1 AND goal > 1000
ORDER BY success_ratio DESC
LIMIT 10;

SELECT * FROM currency;

SELECT (pledged-goal) AS success_diff, name, currency_id
FROM campaign
WHERE pledged-goal > 0 AND goal > 1000
ORDER BY success_diff DESC
LIMIT 10;

SELECT (pledged-goal)*1.25 AS success_diff, name, currency_id
FROM campaign
WHERE pledged-goal > 0 AND goal > 1000 AND currency_id = 1
ORDER BY success_diff DESC
LIMIT 1;

#6
-- Let's try to find successful campaigns in the USA which were backed by investors with big money! 
-- In other words, which campaign has the largest pledges per backer? 
-- Make sure to filter out any null values from your query results

SELECT name, pledged/backers AS PLEDGES_PER_BACKERS
FROM campaign
WHERE currency_id = 2 AND pledged/backers IS NOT null
ORDER BY PLEDGES_PER_BACKERS DESC;
