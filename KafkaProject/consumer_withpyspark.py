
#NOT USING THIS FILE, USING consumer.py INSTEAD

import os
os.environ["HADOOP_HOME"] = ""
os.environ["hadoop.home.dir"] = ""

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

spark = SparkSession.builder \
    .appName("LogProcessor") \
    .master("local[*]") \
    .config("spark.sql.streaming.checkpointLocation", "C:/spark_checkpoints") \
    .config(
        "spark.jars.packages",
        "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1"
    ) \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "logs") \
    .option("startingOffsets", "latest") \
    .load()

json_df = df.selectExpr("CAST(value AS STRING) as json_str")

schema = StructType([
    StructField("service", StringType()),
    StructField("level", StringType()),
    StructField("message", StringType()),
    StructField("response_time", IntegerType()),
    StructField("user_id", StringType()),
    StructField("timestamp", LongType())
])

logs_df = json_df.select(
    from_json(col("json_str"), schema).alias("data")
).select("data.*")

def write_to_postgres(batch_df, batch_id):
    batch_df.write \
        .mode("append") \
        .jdbc(
            url="jdbc:postgresql://localhost:5432/test_db",
            table="logs",
            properties={
                "user": "postgres",
                "password": "postgres",
                "driver": "org.postgresql.Driver"
            }
        )

query = logs_df.writeStream \
    .foreachBatch(write_to_postgres) \
    .option("checkpointLocation", "C:/spark_checkpoints/logs") \
    .outputMode("append") \
    .start()

query.awaitTermination()