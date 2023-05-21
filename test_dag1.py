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
    'owner': 'DummyU',
    'start_date': days_ago(0),
    'email': ['dummy@somemail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# defining the DAG

# define the DAG
dag = DAG(
    'ETL_toll_data',
    default_args=default_args,
    description='EApache Airflow Final Assignment',
    schedule_interval=timedelta(days=1),
)

# the tasks

# dowloading txt file from external resource
download = BashOperator(
    task_id='dowload',
    bash_command='wget https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0250EN-SkillsNetwork/labs/Apache%20Airflow/Build%20a%20DAG%20using%20Airflow/web-server-access-log.txt',
    dag=dag,
)

unzip_data = BashOperator(
    task_id='unzip_data',
    bash_command='sudo tar -xvf /home/project/airflow/dags/finalassignment/tolldata.tgz -C /home/project/airflow/dags/finalassignment',
    dag=dag,
)

extract_data_from_csv = BashOperator(
    task_id='extract_data_from_csv',
    bash_command='cut -d"," -f1-4 /home/project/airflow/dags/finalassignment/vehicle-data.csv > /home/project/airflow/dags/finalassignment/csv_data.csv',
    dag=dag,
)

extract_data_from_tsv = BashOperator(
    task_id='extract_data_from_tsv',
    bash_command='cut -d"\t" -f5-7 /home/project/airflow/dags/finalassignment/tollplaza-data.tsv | tr "\t" "," > /home/project/airflow/dags/finalassignment/tsv_data.csv',
    dag=dag,
)

extract_data_from_fixed_width = BashOperator(
    task_id='extract_data_from_fixed_width',
    bash_command='cat /home/project/airflow/dags/finalassignment/payment-data.txt | rev | cut -d" " -f1,2 | rev | tr " " "," > /home/project/airflow/dags/finalassignment/fixed_width_data.csv',
    dag=dag,
)

consolidate_data = BashOperator(
    task_id='consolidate_data',
    bash_command='paste /home/project/airflow/dags/finalassignment/csv_data.csv /home/project/airflow/dags/finalassignment/tsv_data.csv /home/project/airflow/dags/finalassignment/fixed_width_data.csv > /home/project/airflow/dags/finalassignment/extracted_data.csv',
    dag=dag,
)

transform_data = BashOperator(
    task_id='transform_data',
    bash_command='cat -d"," -f4 /home/project/airflow/dags/finalassignment/extracted_data.csv | tr "[:lower:]" "[:upper:]" > /home/project/airflow/dags/finalassignment/transformed_data.csv',
    dag=dag,
)


# task pipeline
unzip_data >> extract_data_from_csv >> extract_data_from_tsv >> extract_data_from_fixed_width \
    >> consolidate_data >> transform_data
    
    
    