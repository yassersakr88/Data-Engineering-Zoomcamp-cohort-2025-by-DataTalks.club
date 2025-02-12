## Creating External table from uploaded datasets
```BigQuery
-- Creating external table referring to gcs path
CREATE OR REPLACE EXTERNAL TABLE `terraform-demo-449119.nytaxi.external_yellow_tripdata_2024`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://terraform-demo-449119-terra-bucket/trip_data/yellow_tripdata_2024-*.parquet']
);

-- Create regular table
CREATE or REPLACE TABLE `terraform-demo-449119.nytaxi.yellow_tripdata_2024` AS
SELECT *
FROM `terraform-demo-449119.nytaxi.external_yellow_tripdata_2024`;

-- Creating materialized table
CREATE MATERIALIZED VIEW `terraform-demo-449119.nytaxi.yellow_tripdata_2024_materialized` AS
SELECT *
FROM `terraform-demo-449119.nytaxi.external_yellow_tripdata_2024`;
```

## Question 1: What is count of records for the 2024 Yellow Taxi Data?
```BigQuery
-- Check count of records for the 2024 Yellow Taxi Data
SELECT COUNT(*)
FROM terraform-demo-449119.nytaxi.yellow_tripdata_2024;

-- Answer -> 20332093
```

## Question 2:
Write a query to count the distinct number of PULocationIDs for the entire dataset on both the tables.
What is the estimated amount of data that will be read when this query is executed on the External Table and the Table?
*/
```BigQuery
-- as external table
CREATE or REPLACE TABLE `terraform-demo-449119.nytaxi.yellow_tripdata_2024` AS
SELECT PULocationID, COUNT(DISTINCT PULocationID) AS distinct_pulocationids_count
FROM `terraform-demo-449119.nytaxi.external_yellow_tripdata_2024`
GROUP BY PULocationID;
-- Answer ->  0 MB

-- as regular table
SELECT PULocationID, COUNT(DISTINCT PULocationID) AS distinct_pulocationids_count
FROM `terraform-demo-449119.nytaxi.yellow_tripdata_2024`
GROUP BY PULocationID;
-- Answer ->  155.12 MB

-- as materialized table
CREATE MATERIALIZED VIEW `terraform-demo-449119.nytaxi.materialized_yellow_tripdata_2024` AS
SELECT *
FROM `terraform-demo-449119.nytaxi.yellow_tripdata_2024`;
-- Answer ->  0 MB
```

## Question 3:
Why are the estimated number of Bytes different? 

Answer -> BigQuery is a columnar database, and it only scans the specific columns requested in the query. Querying two columns (PULocationID, DOLocationID) requires reading more data than querying one column (PULocationID), leading to a higher estimated number of bytes processed.


## Question 4:
How many records have a fare_amount of 0?
```BigQuery
SELECT COUNT(*) AS ZERO_FARE_COUNT
FROM `terraform-demo-449119.nytaxi.external_yellow_tripdata_2024`
WHERE fare_amount = 0;
-- Answer -> 8333
```

## Question 5:
What is the best strategy to make an optimized table in Big Query if your query will always filter based on tpep_dropoff_datetime and order the results by VendorID (Create a new table with this strategy)
```BigQuery
-- Answer -> Partition by tpep_dropoff_datetime and Cluster on VendorID
```
## Question 6:
Write a query to retrieve the distinct VendorIDs between tpep_dropoff_datetime 2024-03-01 and 2024-03-15 (inclusive)

Use the materialized table you created earlier in your from clause and note the estimated bytes. Now change the table in the from clause to the partitioned table you created for question 5 and note the estimated bytes processed. What are these values?

```BigQuery
SELECT DISTINCT(VendorID)
FROM `terraform-demo-449119.nytaxi.materialized_yellow_tripdata_2024`
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' AND '2024-03-15';
-- Answer -> distinct VendorIDs are 6, 2, 1
-- process 310.24 MB

-- Creating a partition and cluster table
CREATE OR REPLACE TABLE 'terraform-demo-449119.nytaxi.yellow_tripdata_2024_partitioned_clustered'
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID AS
SELECT * FROM 'terraform-demo-449119.nytaxi.external_yellow_tripdata_2024';

SELECT DISTINCT(VendorID)
FROM `terraform-demo-449119.nytaxi.yellow_tripdata_2024_partitioned_clustered`
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' AND '2024-03-15';
-- Answer -> distinct VendorIDs are 2, 1, 6
-- process 26.84 MB
```

## Question 7. Where is the data for external tables stored? (1 point)
```BigQuery
-- Answer -> GCP Bucket
```

## Question 8. Always clustering (1 point)
```BigQuery
False
```
