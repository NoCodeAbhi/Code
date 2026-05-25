from kafka import KafkaConsumer
import json
import psycopg2
from datetime import datetime

#Kafka Consumer

consumer = KafkaConsumer(
    "logs",
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='latest',
    enable_auto_commit=True,
)

#PostgreSQL connection

conn = psycopg2.connect(
    host="localhost",
    database="testdb",
    password = "postgres",
    user = "postgres",
    port = 5432
)

cursor = conn.cursor()

print("Consumer is listening to Kafka topic 'logs'...")

for message in consumer:
    log = message.value
    print("Received log:", log)

    #Insert into db

    insert_query = """
    INSERT INTO logs (service, level, message, response_time, user_id, timestamps)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(insert_query, (
        log['service'],
        log['level'],
        log['message'],
        log['response_time'],
        log['user_id'],
        datetime.fromtimestamp(log["timestamp"]) 
    ))
    print("Inserted log into PostgreSQL database.")
    conn.commit()