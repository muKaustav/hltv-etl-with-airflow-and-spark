import json
import pandas as pd
import boto3
from datetime import datetime

PATH = "/home/ubuntu/airflow/hltv_dags/pipeline/data/"

client = boto3.client("s3")
bucket_name = "etl-s3-airflow"


def convert_date_to_str(timestamp):
    timestamp_s = timestamp / 1000
    dt = datetime.utcfromtimestamp(timestamp_s)
    formatted_date = dt.strftime("%Y-%m-%dT%H:%M:%SZ")

    return formatted_date


def run_hltv_etl():
    with open(PATH + "news.json") as f:
        data = json.load(f)
        df = pd.DataFrame(data)

        for index, row in df.iterrows():
            df.loc[index, "country_name"] = row["country"]["name"]
            df.loc[index, "country_code"] = row["country"]["code"]
            df.loc[index, "publishedAt"] = convert_date_to_str(row["date"])

        df.dropna(inplace=True)

        df = df.drop(["country", "date"], axis=1)

        df.to_csv(PATH + "news.csv", index=False)
        
        status_dict = {
            "status": "success",
            "message": "File transformed successfully",
        }

        print(status_dict)
