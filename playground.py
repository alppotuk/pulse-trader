import os
from dotenv import load_dotenv

load_dotenv("config/.env")
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")
print("Kafka bootstrap servers:", os.getenv("KAFKA_BOOTSTRAP_SERVERS"))