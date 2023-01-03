from datetime import datetime,timedelta

from airflow import DAG

default_args = {
    'owner': 'root',
    'start_date': datetime(2022,3,4),
    'retries': 0,
    'retry_delay': timedelta(minutes=0)
}

hello_word_dag = DAG(
    'hello_world_dag',
    default_args = default_args,
    description='Hello World DAG',
    schedule_interval='* * * * *',
    catchup=False,
    tags=['example,helloworld'])
