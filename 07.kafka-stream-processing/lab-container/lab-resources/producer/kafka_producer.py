import time
import csv
import json
import logging
import argparse
from kafka import KafkaProducer
from kafka.errors import KafkaError

def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)s: %(message)s'
    )

def parse_args():
    parser = argparse.ArgumentParser(description="CSV to Kafka Producer")
    parser.add_argument('--brokers', default='kafka01:9092,kafka02:9092',
                        help='Comma-separated list of Kafka brokers')
    parser.add_argument('--topic', default='demo-nyc-taxi-fare',
                        help='Kafka topic to send messages to')
    parser.add_argument('--csv', default='data.csv',
                        help='Path to input CSV file')
    parser.add_argument('--delay', type=float, default=1.0,
                        help='Delay between messages (seconds)')
    return parser.parse_args()

def main():
    setup_logger()
    args = parse_args()
    brokers = [b.strip() for b in args.brokers.split(',')]
    topic = args.topic
    csv_path = args.csv
    delay = args.delay

    try:
        producer = KafkaProducer(
            bootstrap_servers=brokers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            retries=5,
            linger_ms=10
        )
    except Exception as e:
        logging.error(f"Failed to create KafkaProducer: {e}")
        return

    try:
        with open(csv_path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    future = producer.send(topic, value=row)
                    record_metadata = future.get(timeout=10)
                    logging.info(f"Sent to {record_metadata.topic} partition {record_metadata.partition}: {row}")
                except KafkaError as ke:
                    logging.error(f"Failed to send message: {ke}")
                time.sleep(delay)
    except FileNotFoundError:
        logging.error(f"CSV file not found: {csv_path}")
    except Exception as e:
        logging.error(f"Error reading CSV or sending messages: {e}")
    finally:
        producer.flush()
        producer.close()
        logging.info("Producer closed.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Script interrupted by user. Exiting gracefully.")
