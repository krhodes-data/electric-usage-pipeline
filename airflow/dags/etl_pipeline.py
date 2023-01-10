from datetime import datetime

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator

from dataClean import run_all
from dataMine import download_csv_raw
from uploadToGCS import upload_to_gcs

def say_hello():
    print("Hello!")

default_args = {
    'owner': 'krhodes',
    'email': 'krhodes.data@gmail.com',
    'start_date': datetime.today(),
    'retries': 1
}

etl_dag = DAG(
    dag_id='etl_pipeline',
    default_args=default_args
)

hello_world_task = PythonOperator(
    task_id='hello_world_task',
    python_callable=say_hello,
    dag=etl_dag
)

data_mine = PythonOperator(
    task_id='data_mine',
    python_callable=download_csv_raw,
    dag=etl_dag
)

data_clean = PythonOperator(
    task_id='data_clean',
    python_callable=run_all,
    dag=etl_dag
)

data_upload = PythonOperator(
    task_id='data_upload',
    python_callable=upload_to_gcs,
    dag=etl_dag,
    retries=5,
    trigger_rule='all_done'
)

data_mine >> data_clean >> data_upload