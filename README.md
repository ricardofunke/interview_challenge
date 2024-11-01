# interview_challenge

## Requirements
- Java 17
- Python 3.11

```
pip install pyspark==3.5.1
pip install findspark==2.0.1
pip install pandas==2.2.2
```

## Instructions
Simply install all the requirements above and run the script with the CSV as its single parameter, for example:

```
$ python run_query_fire_data.py data/Fire_Incidents_20241031.csv
```

You must manually download the CSV file from the source first.

## Description
This code demonstrate the use of Spark to simulate data ingestion into a dummy data warehouse.

The purpose is to show how data can be stored using bucket partitioning to have better query performance.

The code is very simple and it basically reads data from a CSV file and writes its data in multiple parquet files (data warehouse).

There are at least 2 techniques used here to demonstrate data storing:
1. parquet files: this file format provides columnar partitioning which results in efficient storage sizes and better performance on data querying by permiting parallel retrieving from the selected data.
2. bucketed data: this method can also improve data querying by organizing data in multiple files by hashed columns tables their most used columns for querying, which permits parallel processing of the data. This method is appropriate in cases where the main columns has a huge amount of unique values in contrast with simple columnar partitioning which can be used where there are a small number of unique values to query.

When storing the data, it is previously sellected the main columns which the buckets should be generated from, based on the users analysing requests:
"Incident Number", "Incident Date", "Supervisor District", "Battalion"

Then it is provided a simple command-line interface to simulate SQL queries inserted by the users to get results from this database.

## Limitations
This program simulates the ingestion of one single CSV file at a time, it cannot append multiple different CSV files into the same database. For this, it would require a Delta Lake or Hive metastore which is beyond the intentions of this program.

For this reason, it will always destroy the database before each execution.

This program uses a very simple implementation to allow SQL queries from the user. Its intention is to merely simulates how data can be retrieved from the data warehouse using SQL.

