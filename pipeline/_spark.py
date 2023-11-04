import os
from decouple import config
import boto3
from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    IntegerType,
    TimestampType,
)
from pyspark.sql.functions import count, avg, max

client = boto3.client("s3")
bucket_name = config("S3_BUCKET_NAME")

PATH = "/home/ubuntu/airflow/hltv_dags/pipeline/data/"

schema = StructType(
    [
        StructField("link", StringType(), True),
        StructField("title", StringType(), True),
        StructField("comments", IntegerType(), True),
        StructField("country_name", StringType(), True),
        StructField("country_code", StringType(), True),
        StructField("publishedAt", TimestampType(), True),
    ]
)


def main(spark):
    df = spark.read.schema(schema).csv(PATH + "/news.csv")
    df = df.select("title", "comments", "country_name")

    country_stats = df.groupBy("country_name").agg(
        count("title").alias("total_articles"),
        avg("comments").alias("avg_comments"),
        max("comments").alias("max_comments"),
    )

    country_stats.show()

    stats_df = country_stats.toPandas()
    stats_df.to_csv(PATH + "stats.csv", index=False)

    try:
        client.upload_file(
            Filename=PATH + "stats.csv",
            Bucket=bucket_name,
            Key=f"stats_{str(datetime.now().year)}_{str(datetime.now().month)}.csv",
        )

        status_dict = {
            "status": "success",
            "message": "File uploaded successfully",
        }

        print(status_dict)

    except Exception as e:
        status_dict = {
            "status": "failure",
            "error": str(e),
            "message": "Error writing to S3",
        }

        print(status_dict)


if __name__ == "__main__":
    spark = SparkSession.builder.appName("run_analytics").getOrCreate()

    try:
        main(spark)

    finally:
        spark.stop()

