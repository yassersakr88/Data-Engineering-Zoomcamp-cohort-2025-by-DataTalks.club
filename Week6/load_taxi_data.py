import pandas as pd
import json
from kafka import KafkaProducer
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # Create a Kafka producer
    producer = KafkaProducer(
        bootstrap_servers='localhost:9092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        compression_type='gzip'  # Enable compression
    )
    
    t0 = time.time()

    csv_file = 'green_tripdata_2019-10.csv.gz'
    col = ['lpep_pickup_datetime', 'lpep_dropoff_datetime', 'PULocationID', 'DOLocationID', 'passenger_count', 'trip_distance', 'tip_amount']
    
    # Read CSV in chunks for memory efficiency
    chunksize = 100000
    total_messages = 0

    topic_name = 'green-trips'
    
    logger.info(f"Starting to send messages to Kafka topic '{topic_name}'")

    for chunk in pd.read_csv(csv_file, usecols=col, chunksize=chunksize):
        for i, row in enumerate(chunk.itertuples(index=False), start=1):
            row_dict = row._asdict()
            try:
                producer.send(topic_name, value=row_dict)
            except Exception as e:
                logger.error(f"Failed to send message: {e}")
            
            if i % 10000 == 0:  # Print progress every 10,000 rows
                logger.info(f"Sent {i} messages...")
        
        total_messages += len(chunk)

    # Make sure any remaining messages are delivered
    producer.flush()
    producer.close()
    
    t1 = time.time()
    logger.info(f"Finished sending {total_messages} messages. Took {(t1 - t0):.2f} seconds")

if __name__ == "__main__":
    main()