## Module 2 Homework: Workflow Orchestration

## Question 1. Within the execution for Yellow Taxi data for the year 2020 and month 12: what is the uncompressed file size (i.e. the output file yellow_tripdata_2020-12.csv of the extract task)?

Answer -> 128.3 MB

![Screenshot 2025-02-02 190019](https://github.com/user-attachments/assets/489d1291-a454-4072-b53f-d422d8537bbf)

## Question 2. What is the rendered value of the variable file when the inputs taxi is set to green, year is set to 2020, and month is set to 04 during execution?

Answer -> green_tripdata_2020-04.csv

![Screenshot 2025-02-02 191010](https://github.com/user-attachments/assets/1e90386e-2b1a-4fd8-887f-a27ab23d93b5)

## Question 3. How many rows are there for the Yellow Taxi data for all CSV files in the year 2020?
Answer -> 24,648,499
```postgres
SELECT count(*) 
FROM public.yellow_tripdata
WHERE filename LIKE '%2020%';
```

## Question 4. How many rows are there for the Green Taxi data for all CSV files in the year 2020?

Answer -> 1,734,051
```postgres
SELECT count(*) 
FROM public.green_tripdata
WHERE filename LIKE '%2020%';
```

## Question 5. How many rows are there for the Yellow Taxi data for the March 2021 CSV file?
Answer -> 1,925,152
```postgres
SELECT count(*) 
FROM public.yellow_tripdata
WHERE filename LIKE 'yellow_tripdata_2021-03.csv';
```

## Question 6. How would you configure the timezone to New York in a Schedule trigger?

Answer -> Add a timezone property set to America/New_York in the Schedule trigger configuration

```yaml
triggers:
  - id: green_schedule
    type: io.kestra.plugin.core.trigger.Schedule
    cron: "0 9 1 * *"
    timezone: "America/New_York"
    inputs:
      taxi: green
```
