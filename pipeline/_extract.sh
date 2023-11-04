echo "extraction started"

cd /home/ubuntu/airflow/hltv_dags/pipeline

echo "downloading data"

node extract_hltv_news.js

echo "extraction finished"

mv news.json data/

echo "moved file to data/ folder"
