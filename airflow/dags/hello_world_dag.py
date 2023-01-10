#datetime
from datetime import timedelta, datetime

# The DAG object
from airflow import DAG

# Operators
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator

# initializing the default arguments
default_args = {
		'owner': 'Ranga',
		'start_date': datetime(2022, 3, 4),
		'retries': 3,
		'retry_delay': timedelta(minutes=5)
}

# Instantiate a DAG object
hello_world_dag = DAG('hello_world_dag',
		default_args=default_args,
		description='Hello World DAG',
		schedule_interval='* * * * *', 
		catchup=False,
		tags=['example, helloworld']
)

# python callable function
def print_hello():
		return 'Hello World!'

# Creating first task
start_task = DummyOperator(task_id='start_task', dag=hello_world_dag)

# Creating second task
hello_world_task = PythonOperator(task_id='hello_world_task', python_callable=print_hello, dag=hello_world_dag)

# Creating third task
end_task = DummyOperator(task_id='end_task', dag=hello_world_dag)

start_task >> hello_world_task >> end_task



#DataCamp learning

from airflow.models import DAG

from datetime import datetime

default_arguments = {
	'owner': 'krhodes',
	'email': 'krhodes-data@gmail.com',
	'start_date': datetime(2020,1,20)
}
etl_dag = DAG(
	dag_id='test_dag',
	default_args=default_args
)