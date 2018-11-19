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
    'retries': 100,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG('terraform', default_args=default_args, schedule_interval=timedelta(minutes=10))

terraform_command = """
    cd ~/terraform_ex/with_code/
    terraform init
    terraform apply -auto-approve
    ip=$(terraform output ip)
"""

t1 = BashOperator(
    task_id='templated',
    bash_command=terraform_command,
    dag=dag)
