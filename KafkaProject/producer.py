#create kafka producer

from kafka import KafkaProducer
import json
import random
import time

current_timestamp = int(time.time() * 1000)

producer = KafkaProducer(bootstrap_servers='localhost:9092',
                         value_serializer=lambda v: json.dumps(v).encode('utf-8')
                    )

services = ["auth", "payment", "orders", "search"]
levels = ["INFO", "WARN", "ERROR"]

while True:
    log = {
    "service": random.choice(services),
    "level": random.choice(levels),
    "message": "Payment failed due to timeout",
    "response_time": 1200,
    "user_id": "U123",
    "timestamp": int(time.time())
    }
    producer.send('logs', value=log)
    print("Sent log:", log)
    time.sleep(5)