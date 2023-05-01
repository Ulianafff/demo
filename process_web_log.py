# import the libraries

from datetime import timedelta
# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG
# Operators; we need this to write tasks!
from airflow.operators.bash_operator import BashOperator
# This makes scheduling easy
from airflow.utils.dates import days_ago

#defining DAG arguments

# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'Ulianafff',
    'start_date': days_ago(0),
    'email': ['uman@somemail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# defining the DAG

# define the DAG
dag = DAG(
    'process_web_log',
    default_args=default_args,
    description='Process WEB log',
    schedule_interval=timedelta(minutes=1),
)

# define the tasks

# take 1st column with Space symbol delimeter (ip address) and copy to extracted_data.txt

extract_data = BashOperator(
    task_id='extract',
    bash_command='cut -d" " -f1 /home/project/airflow/dags/capstone/accesslog.txt > /home/project/airflow/dags/capstone/extracted_data.txt',
    dag=dag,
)

# remove all records with ip = 198.46.149.143
transform_data = BashOperator(
    task_id='transform',
    bash_command='grep -v 198.46.149.143 < /home/project/airflow/dags/capstone/extracted_data.txt > /home/project/airflow/dags/capstone/transformed_data.txt',
    dag=dag,
)

# archive the result
load_data = BashOperator(
    task_id='load',
    bash_command='tar -czvf weblog.tar /home/project/airflow/dags/capstone/transformed_data.txt',
    dag=dag,
)

# task pipeline
extract_data >> transform_data >> load_data