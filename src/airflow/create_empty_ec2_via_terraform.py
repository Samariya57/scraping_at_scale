import random
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2018, 6, 1),
    'email': ['masha@insightdatascience.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 10,
    'retry_delay': timedelta(minutes=random.randint(1, 10)),
}

dag = DAG('empty_ec2', default_args=default_args, schedule_interval=timedelta(days=1))

terraform_command = """
    terraform init
    terraform apply
"""

t1 = BashOperator(
    task_id='templated',
    bash_command=terraform_command,
    dag=dag)
