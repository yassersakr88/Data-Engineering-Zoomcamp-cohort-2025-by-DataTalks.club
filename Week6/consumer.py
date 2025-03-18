from kafka import KafkaConsumer
import json

def consume_messages():
    # Create a Kafka consumer
    consumer = KafkaConsumer(
        'green-trips',  # Topic name
        bootstrap_servers='localhost:9092',  # Kafka broker address
        auto_offset_reset='earliest',  # Start reading from the beginning of the topic
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))  # Deserialize JSON messages
        )
    print("Starting to consume messages...")
    for message in consumer:
        print(message.value)  # Print each message

if __name__ == "__main__":
    consume_messages()