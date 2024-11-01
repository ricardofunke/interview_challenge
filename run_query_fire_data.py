import shutil
import sys
import os
from pyspark.sql import SparkSession
import findspark


findspark.init()

spark = SparkSession\
            .builder\
            .appName("FireIncidents")\
            .config("spark.sql.shuffle.partitions", 8)\
            .config("spark.default.parallelism", 8)\
            .master("local[2]")\
            .getOrCreate()


def load_file(csv_file):
    raw_fireincidents_data = spark\
                            .read\
                            .option("inferSchema", "true")\
                            .option("header", "true")\
                            .csv(csv_file)

    raw_fireincidents_data.write\
                        .mode('overwrite')\
                        .format("parquet")\
                        .bucketBy(8, ["Incident Number", "Incident Date", "Supervisor District", "Battalion"])\
                        .saveAsTable("fireincidents", mode='overwrite')
    

def run_query(query):
    print('wait...')
    spark.sql(query).show()


if __name__ == '__main__':
    shutil.rmtree('spark-warehouse', ignore_errors=True)

    print()
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <fire_incidents_report.csv>: {len(sys.argv)}")
        sys.exit(1)

    input_file = sys.argv[-1]

    if not os.path.isfile(input_file):
        print(f"Invalid file: {input_file}")
        sys.exit(1)

    load_file(input_file)

    print()
    print("Type query below ('.' to run query, Ctrl-D to exit):")
    print("Table name is: fireincidents")
    print()
    query = []
    while True:
        try:
            line = input()
        except EOFError:
            break

        if line == '.':
            if query:
                run_query(' '.join(query))
                query.clear()
        else:
            if line.strip():
                query.append(line)
