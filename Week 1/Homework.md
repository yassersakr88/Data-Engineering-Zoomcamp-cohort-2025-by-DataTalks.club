## Module 1 Homework: Docker & SQL

## Question 1. Understanding docker first run 
$ docker container run -it python:3.12.8 bash
root@7b10fb5682be:/# pip --version
pip 24.3.1 from /usr/local/lib/python3.12/site-packages/pip (python 3.12)

## Question 2. Understanding Docker networking and docker-compose
postgres:5433

## Question 3. Trip Segmentation Count
/*
During the period of October 1st 2019 (inclusive) and November 1st 2019 (exclusive),
how many trips, respectively, happened:
*/
-- Answer: 104802, 198924, 109603, 27678, 35189

-- Up to 1 mile
SELECT COUNT(*) AS no_of_trips
FROM public.green_taxi_trips
WHERE CAST (lpep_dropoff_datetime AS date) BETWEEN '2019-10-01' AND '2019-10-31'
AND trip_distance <= 1;
-- 104802

-- In between 1 (exclusive) and 3 miles (inclusive)
SELECT COUNT(*) AS no_of_trips
FROM public.green_taxi_trips
WHERE CAST (lpep_dropoff_datetime AS date) BETWEEN '2019-10-01' AND '2019-10-31'
AND trip_distance > 1 AND trip_distance <= 3;
-- 198924

-- In between 3 (exclusive) and 7 miles (inclusive)
SELECT COUNT(*) AS no_of_trips
FROM public.green_taxi_trips 
WHERE CAST (lpep_dropoff_datetime AS date) BETWEEN '2019-10-01' AND '2019-10-31'
AND trip_distance > 3 AND trip_distance <= 7;
-- 109603

-- In between 7 (exclusive) and 10 miles (inclusive)
SELECT COUNT(*) AS no_of_trips
FROM public.green_taxi_trips 
WHERE CAST (lpep_dropoff_datetime AS date) BETWEEN '2019-10-01' AND '2019-10-31'
AND trip_distance > 7 AND trip_distance <= 10;
-- 27678

-- Over 10 miles
SELECT COUNT(*) AS no_of_trips
FROM public.green_taxi_trips
WHERE CAST (lpep_dropoff_datetime AS date) BETWEEN '2019-10-01' AND '2019-10-31'
AND trip_distance > 10;
-- 35189

## Question 4. Longest trip for each day
/*
Which was the pick up day with the longest trip distance? Use the pick up time for your calculations.

Tip: For every day, we only care about one single trip with the longest distance.

2019-10-11
2019-10-24
2019-10-26
2019-10-31
*/

SELECT CAST (lpep_pickup_datetime AS date) AS pickup_date, MAX(trip_distance) AS longest_trip
FROM public.green_taxi_trips
WHERE CAST (lpep_pickup_datetime AS date) IN ('2019-10-11', '2019-10-24', '2019-10-26', '2019-10-31')
GROUP BY pickup_date
ORDER BY longest_trip DESC
LIMIT 1;
-- 2019-10-31, 515.89

## Question 5. Three biggest pickup zones
/*
Which were the top pickup locations with over 13,000 in total_amount (across all trips) for 2019-10-18?

Consider only lpep_pickup_datetime when filtering by date.

East Harlem North, East Harlem South, Morningside Heights
East Harlem North, Morningside Heights
Morningside Heights, Astoria Park, East Harlem South
Bedford, East Harlem North, Astoria Park
*/
SELECT z."Zone" AS pickup_zone, SUM(t.total_amount) AS total_per_zone
FROM public.green_taxi_trips t
JOIN taxi_zones_lookup z ON t."PULocationID" = z."LocationID"
WHERE CAST (lpep_pickup_datetime AS date) = '2019-10-18'
GROUP BY pickup_zone
HAVING SUM(t.total_amount) > 13000
ORDER BY total_per_zone DESC
LIMIT 3;
-- East Harlem South, 18686.68
-- East Harlem South, 16797.26
-- Morningside Heights,13029.79

## Question 6. Largest tip
/*
For the passengers picked up in October 2019 in the zone named "East Harlem North" which was the drop off zone that had the largest tip?

Note: it's tip , not trip

We need the name of the zone, not the ID.

Yorkville West
JFK Airport
East Harlem North
East Harlem South
*/
SELECT zdo."Zone" AS dropoff_zone, t.tip_amount
FROM public.green_taxi_trips t
JOIN taxi_zones_lookup zpu ON t."PULocationID" = zpu."LocationID"
JOIN taxi_zones_lookup zdo ON t."DOLocationID" = zdo."LocationID"
WHERE CAST (lpep_dropoff_datetime AS date) <= '2019-10-31' AND
zpu."Zone" = 'East Harlem North'
GROUP BY dropoff_zone, t.tip_amount
ORDER BY t.tip_amount DESC
LIMIT 1;
--JFK Airport, 87.3

## Question 7. Terraform Workflow
Which of the following sequences, respectively, describes the workflow for:

Downloading the provider plugins and setting up backend,
Generating proposed changes and auto-executing the plan
Remove all resources managed by terraform

-- terraform init, terraform apply -auto-approve, terraform destroy
