---
duration: 1h
---

# Lab: Data Streaming ETL pipeline with Kafka and NiFi

- Build a real-time data streaming ETL pipeline with NiFi and Kafka.

## Tasks

1. Configuration of Kafka producer and consume messages with NiFi.
2. Build the dataflow.

## Prerequisites

- Completion of the [Introduction to Kafka lab](../../../bigdata/modules/06.kafka-stream-processing/lab-container/lab-introduction-to-kafka.md)

- Completion of the [Introduction to NiFi lab](../01.nifi-dataflow/lab-introduction-to-nifi.md) and [NiFi ETL pipeline](./lab-02-build-ETL-pipeline.md).

## Build consumer in NiFi

1. Use the "ConsumeKafka" processor to consume Kafka messages. Configure the processor with the following values:

    ```
    - Kafka Connection Service: Kafka3ConnectionService
    - Group ID: nifi-CG-01
    - Topic Name(s): demo-nyc-taxi-fare
    - Processing Strategy: RECORD
    - Value Record Reader: JsonTreeReader
    - Record Value Writer: JsonRecordSetWriter
    ```

2. Configure "Kafka3ConnectionService" controller:

    ```
    - Bootstrap Servers: lab-kafka01:9092,lab-kafka02:9092
    ```

Enable the controller after configuration.

3. Define dataset schema in a parameter context.

- Click on the "Configuration" of the current process group, and click the "+" button next to "Parameter Context".

    ```
    - Name: lab-kafka-nifi
    ```

- add a new parameter:

    ```
    - Name: avro.schema.nycdriver.raw
    {
        "type" : "record",
        "name" : "nyc_taxi",
        "fields" : [
            { "name": "VendorID", "type": "string" },
            { "name": "tpep_pickup_datetime", "type": "string" },
            { "name": "tpep_dropoff_datetime", "type": "string" },
            { "name": "passenger_count", "type": "string" },
            { "name": "trip_distance", "type": "string" },
            { "name": "RatecodeID", "type": "string" },
            { "name": "store_and_fwd_flag", "type": "string" },
            { "name": "PULocationID", "type": "string" },
            { "name": "DOLocationID", "type": "string" },
            { "name": "payment_type", "type": "string" },
            { "name": "fare_amount", "type": "string" },
            { "name": "extra", "type": "string" },
            { "name": "mta_tax", "type": "string" },
            { "name": "tip_amount", "type": "string" },
            { "name": "tolls_amount", "type": "string" },
            { "name": "improvement_surcharge", "type": "string" },
            { "name": "total_amount", "type": "string" },
            { "name": "congestion_surcharge", "type": "string" }
        ]
    }
    ```

4. Configure 2 Json controllers. Note that "Schema Access Strategy" should be "Use 'Schema Text' Property" and provide an avro schema for the controller. Enable 2 controllers after configuration.

- Schema Access Strategy: `Use 'Schema Text' Property`
- Schema Text: `#{avro.schema.nycdriver.raw}`

4. Set connection "success" and "parse failure" to temp funnels.

## Build transformation process

1. Transform the data as needed, using at least 3 processors to complete this step.

## Insert into Postgres database

1. Run the following command to launch a Postgres shell:

   ```bash
   docker exec -it lab-postgres /bin/bash
   # inside container
   psql -U <postgres-username> -d <db-name>
   ```

2. Create the target table for data insertion. Please make sure the table schema matches your data.

## Start real-time streaming from the kafka-data-producer container

1. Run the `kafka_producer.py` Python script inside the container to simulate real-time data, and continusly produce messages to the Kafka topic.

    ```bash
    docker exec -it kafka-data-producer /bin/sh
    # Inside the container:
    python kafka_producer.py \
        --brokers lab-kafka01:9092,lab-kafka02:9092 \
        --topic demo-nyc-taxi-fare \
        --csv data.csv \
        --delay 1
    ```

2. Check for any errors in the NiFi UI.

3. Verify that the data appears correctly in the Postgres table.