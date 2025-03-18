## Question 1: Redpanda version
```
redpanda@02413ff6d959:/$ rpk version
Version:     v24.2.18
Git ref:     f9a22d4430
Build date:  2025-02-14T12:52:55Z
OS/Arch:     linux/amd64
Go version:  go1.23.1

Redpanda Cluster
  node-1  v24.2.18 - f9a22d443087b824803638623d6b7492ec8221f9
```

## Question 2. Creating a topic
```
redpanda@02413ff6d959:/$ rpk topic create green-trips
TOPIC        STATUS
green-trips  TOPIC_ALREADY_EXISTS: The topic has already been created
```

## Question 3. Connecting to the Kafka server
```
producer.bootstrap_connected()
True
```

## Question 4. Sending data to the stream
How much time did it take? 
Answer -> took 0.51 seconds

Where did it spend most of the time?
Answer -> Sending the messages


## Reading data with rpk
```
redpanda@02413ff6d959:/$ rpk topic consume test-topic
{
  "topic": "test-topic",
  "value": "{\"number\": 0}",
  "timestamp": 1742241606141,
  "partition": 0,
  "offset": 0
}
{
  "topic": "test-topic",
  "value": "{\"number\": 1}",
  "timestamp": 1742241606191,
  "partition": 0,
  "offset": 1
}
{
  "topic": "test-topic",
  "value": "{\"number\": 2}",
  "timestamp": 1742241606242,
  "partition": 0,
  "offset": 2
}
{
  "topic": "test-topic",
  "value": "{\"number\": 3}",
  "timestamp": 1742241606292,
  "partition": 0,
  "offset": 3
}
{
  "topic": "test-topic",
  "value": "{\"number\": 4}",
  "timestamp": 1742241606342,
  "partition": 0,
  "offset": 4
}
{
  "topic": "test-topic",
  "value": "{\"number\": 5}",
  "timestamp": 1742241606393,
  "partition": 0,
  "offset": 5
}
{
  "topic": "test-topic",
  "value": "{\"number\": 6}",
  "timestamp": 1742241606443,
  "partition": 0,
  "offset": 6
}
{
  "topic": "test-topic",
  "value": "{\"number\": 7}",
  "timestamp": 1742241606494,
  "partition": 0,
  "offset": 7
}
{
  "topic": "test-topic",
  "value": "{\"number\": 8}",
  "timestamp": 1742241606544,
  "partition": 0,
  "offset": 8
}
{
  "topic": "test-topic",
  "value": "{\"number\": 9}",
  "timestamp": 1742241606595,
  "partition": 0,
  "offset": 9
}
```

## Sending the taxi data
check load_taxi_data.py


## Question 5: Build a Sessionization Window
```
SELECT
    PULocationID,
    DOLocationID,
    MAX(streak_count) AS longest_streak
FROM
    processed_trips
GROUP BY
    PULocationID,
    DOLocationID
ORDER BY
    longest_streak DESC
LIMIT 10;
```
| pulocationid   | dolocationid   | longest_streak |
|----------------|----------------|----------------|
| 95             | 95             | 44             |
| 7              | 7              | 43             |
| 82             | 138            | 35             |
| 75             | 74             | 33             |
| 74             | 75             | 31             |
| 223            | 223            | 30             |
| 82             | 129            | 24             |
| 74             | 166            | 23             |
| 166            | 166            | 13             |
| 82             | 7              | 13             |

