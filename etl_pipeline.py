import os
from decouple import config
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.contrib.sensors.file_sensor import FileSensor
from airflow.operators.python_operator import PythonOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.operators.email_operator import EmailOperator
from datetime import datetime, timedelta
from pipeline._transform import run_hltv_etl

HOME = config("HOME")
PATH = os.path.join(HOME, "airflow", "hltv_dags", "pipeline")
NOTIF_EMAIL = config("AIRFLOW_EMAIL")


def send_failure_email(context):
    send_email = EmailOperator(
        task_id="send_failure_email",
        to=NOTIF_EMAIL,
        subject="Airflow alert: HLTV DAG Failed",
        html_content=f"The HLTV DAG has failed on {str(datetime.today().strftime('%A'))}, {str(datetime.today.strftime('%d/%m/%Y'))} at {str(datetime.today.strftime('%H:%M:%S'))}",
        dag=dag,
    )

    send_email.execute(context)


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2023, 11, 4),
    "email": [NOTIF_EMAIL],
    "email_on_failure": True,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    "hltv_dag",
    default_args=default_args,
    description="A simple DAG to fetch HLTV news, run analytics on it, dump it to a S3 and send an email notification",
    schedule_interval=timedelta(days=1),
    on_failure_callback=send_failure_email,
)

extract_hltv_news = BashOperator(
    task_id="extract_hltv_news",
    bash_command="bash {} ".format(os.path.join(PATH, "_extract.sh")),
    dag=dag,
)

check_downloaded_file = FileSensor(
    task_id="check_downloaded_file",
    fs_conn_id="fs_default",
    filepath=os.path.join(PATH, "data", "news.json"),
    dag=dag,
)

run_etl = PythonOperator(
    task_id="run_etl",
    python_callable=run_hltv_etl,
    dag=dag,
)

spark_analysis = SparkSubmitOperator(
    task_id="spark_analysis",
    application=os.path.join(PATH, "_spark.py"),
    conn_id="spark_default",
    total_executor_cores="2",
    executor_cores="2",
    executor_memory="2g",
    num_executors="2",
    name="run_analytics",
    verbose=1,
    driver_memory="1g",
    dag=dag,
)

clear_temp_files = BashOperator(
    task_id="clear_temp_files",
    bash_command="bash {} ".format(os.path.join(PATH, "_clear.sh")),
    dag=dag,
)

send_email = EmailOperator(
    task_id="send_email",
    to=NOTIF_EMAIL,
    subject="Airflow alert: HLTV DAG Finished Successfully",
    html_content=f"The HLTV DAG has finished successfully on {str(datetime.today().strftime('%A'))}, {str(datetime.today().strftime('%d/%m/%Y'))} at {str(datetime.today().strftime('%H:%M:%S'))}",
    dag=dag,
)

(
    extract_hltv_news
    >> check_downloaded_file
    >> run_etl
    >> spark_analysis
    >> clear_temp_files
    >> send_email
)

