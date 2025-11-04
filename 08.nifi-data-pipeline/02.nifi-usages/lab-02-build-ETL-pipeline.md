---
duration: 2h
---

# Lab: Introduction to NiFi Objectives

- Build an ETL pipeline with the NiFi ui

## Tasks

1. Set up the environment.
2. Configuration of Postgres database.
3. Build the dataflow.

## Prerequisites

- Completion of [Introduction to NiFi lab](../01.nifi-dataflow/lab-introduction-to-nifi.md)

## Set up the environment

1. You will need the following .jar file in NiFi container for accessing the Postgres database, so do the following command in the directory that you have mounted between your local file system and the contianer. Go into the container to get the resource into "/opt/nifi/nifi-current/lib/" folder

   ```bash
   docker exec -it lab-nifi /bin/bash
   ```

   ```bash
   # inside the container
   wget https://repo1.maven.org/maven2/org/postgresql/postgresql/42.2.24/postgresql-42.2.24.jar -O /opt/nifi/nifi-current/lib/postgresql-42.2.24.jar
   chmod 664 /opt/nifi/nifi-current/lib/postgresql-42.2.24.jar
   exit
   ```

2. Restart the container

   ```bash
   docker restart lab-nifi
   ```

## Configuration of Postgres database

1. Get into Postgres container:

   ```bash
   docker exec -it lab-postgres /bin/bash
   ```

2. Inside the container, run the following command to launch a Postgres shell:

   ```bash
   psql -U <postgres-username> -d <db-name>
   ```

3. Create a target table for the data ingestion. Note that the table will depend on the transformation process of the pipeline. 

   <details>
      <summary>
      Hint: Here is one of the example to create a Postgres table.</summary>

      Check the [SQL script](./lab-resources/db_create_table.sql)
   </details>

4. Check if your table is created successfully:

   ```
   \d
   \d nyc_taxi_data
   ```

## Build a dataflow

1. Download the dataset from [NYC Taxi Fare Dataset in Kaggle](https://www.kaggle.com/datasets/diishasiing/revenue-for-cab-drivers?resource=download), and place the CSV file into `nifi-126` container.

   ```bash
      docker cp <target_file_path> <container_id>:<target_dir_path>
   ```

2. Use at least one "UpdateRecord" processor to do basic transformation with the FlowFile.

   For example, you could use 2 "UpdateRecord" processors to create a new column with the summation of the existed 2 columns. Check out this [thread](https://stackoverflow.com/questions/59047115/add-two-columns-together-using-apache-nifi).

3. Use PutDatabaseRecord processor to write the data to Postgres database.

   <details>
      <summary>
      Hint: try to do the configuration yourself before opening this block</summary>

      #### configuration of processor "PutDatabaseRecord"

      - Record Reader: `CSVReader`
      - Statement Type: `INSERT`
      - Database Connection Pooling Service: `DBCPConnectionPool`
      - Table Name: `<table name>`


      #### and in the controller of "DBCPConnectionPool"

      - Database Connection URL: `jdbc:postgresql://<ip addr of the container>:5432/dsti_db`
      - Database Driver Class Name: `org.postgresql.Driver`
      - Database Driver Location(s): `/opt/nifi/nifi-current/lib/postgresql-42.2.24.jar`
      - Database User: `<postgres username>`
      - Password: `<postgres password>`

   </details>

## Reference

[NiFi Expression Language Guide](https://nifi.apache.org/docs/nifi-docs/html/expression-language-guide.html)
