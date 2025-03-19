from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.kafka import FlinkKafkaConsumer
from pyflink.datastream.formats.json import JsonRowDeserializationSchema
from pyflink.common import WatermarkStrategy, Time
from pyflink.common.typeinfo import Types
from pyflink.datastream.window import SessionWindowTimeGapExtractor
from pyflink.datastream.functions import MapFunction, AggregateFunction, WindowFunction
from pyflink.datastream.window import TimeWindow
from pyflink.common import Row
from datetime import datetime

# Define the schema for the Kafka data
schema = {
    "lpep_pickup_datetime": Types.STRING(),
    "lpep_dropoff_datetime": Types.STRING(),
    "PULocationID": Types.INT(),
    "DOLocationID": Types.INT(),
    "passenger_count": Types.INT(),
    "trip_distance": Types.FLOAT(),
    "tip_amount": Types.FLOAT()
}

# Create a StreamExecutionEnvironment
env = StreamExecutionEnvironment.get_execution_environment()

# Define a Kafka consumer
kafka_consumer = FlinkKafkaConsumer(
    topics='green-trips',
    deserialization_schema=JsonRowDeserializationSchema.builder().type_info(Types.ROW(schema)).build(),
    properties={'bootstrap.servers': 'redpanda-1:9092', 'group.id': 'session-window-group'}
)

# Add the Kafka consumer as a source
stream = env.add_source(kafka_consumer)

# Assign watermarks based on lpep_dropoff_datetime with 5-second tolerance
class DropoffTimestampAssigner:
    def extract_timestamp(self, value, record_timestamp):
        dropoff_time = datetime.strptime(value["lpep_dropoff_datetime"], "%Y-%m-%d %H:%M:%S").timestamp()
        return int(dropoff_time * 1000)  # Convert to milliseconds

stream = stream.assign_timestamps_and_watermarks(
    WatermarkStrategy.for_bounded_out_of_orderness(Time.seconds(5))
        .with_timestamp_assigner(DropoffTimestampAssigner())
)

# Define a session window with a 5-minute gap
class SessionGapExtractor(SessionWindowTimeGapExtractor):
    def extract(self, value):
        return 5 * 60 * 1000  # 5 minutes in milliseconds

# Key by pickup and drop-off locations
keyed_stream = stream.key_by(lambda row: (row["PULocationID"], row["DOLocationID"]))

# Apply session window and aggregate
class StreakAggregator(AggregateFunction):
    def create_accumulator(self):
        return 0

    def add(self, value, accumulator):
        return accumulator + 1

    def get_result(self, accumulator):
        return accumulator

    def merge(self, a, b):
        return a + b

class StreakWindowFunction(WindowFunction):
    def apply(self, key, window, inputs, out):
        out.collect((key[0], key[1], len(inputs)))

result = keyed_stream.window(SessionWindowTimeGapExtractor(SessionGapExtractor())) \
    .aggregate(StreakAggregator(), StreakWindowFunction())

# Print the result
result.map(lambda row: f"PULocationID: {row[0]}, DOLocationID: {row[1]}, Streak: {row[2]}", Types.STRING()) \
    .print()

# Execute the job
env.execute("Session Window Job")