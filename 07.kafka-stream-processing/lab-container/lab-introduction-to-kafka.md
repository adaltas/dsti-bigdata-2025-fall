# Lab: Data Streaming with Kafka

- Build a real-time data streaming process using Kafka producer and consumer.

## Tasks

1. Launch a Kafka producer to produce data from source, and consume the message. (Medium)

## Set up the environment

## Lab resources

- Use Docker compose to launch Kafka and data producer container.
- Download the dataset from [NYC Taxi Fare Dataset in Kaggle](https://www.kaggle.com/datasets/diishasiing/revenue-for-cab-drivers?resource=download), and place the CSV file into `./lab-resources/producer/`

## Launch the Docker containers

```bash
cd lab-resources
docker compose up -d
```

## Produce real-time data

1. Examine the `kafka_producer.py` to see how to implement Kafka package with Python.

2. Run `kafka_producer.py` python script inside a container to simulate real-time data, and continusly produce to a Kafka topic.

    ```bash
    docker exec -it lab-kafka-data-producer /bin/sh
    # Inside the container:
    python producer.py \
        --brokers lab-kafka01:9092,lab-kafka02:9092 \
        --topic demo-nyc-taxi-fare \
        --csv data.csv \
        --delay 1
    ```

## Consume Kafka messages

1. Open another terminal window and run the following command to see the consuming process.

    ```bash
    docker exec -it lab-kafka01 kafka-console-consumer.sh \
                --bootstrap-server lab-kafka01:9092,lab-kafka02:9092 \
                --topic demo-nyc-taxi-fare \
                --from-beginning \
                --timeout-ms 10000
    ```

