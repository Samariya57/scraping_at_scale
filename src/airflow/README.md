# Airflow
## What it does?
Airflow is a platform to programmatically author, schedule and monitor workflows.

In this project created only one Airflow job (DAG) that triggers preconfigured Tensorflow script every 10 minutes

## How to install?
Please follow [these](https://medium.com/a-r-g-o/installing-apache-airflow-on-ubuntu-aws-6ebac15db211) instructions, use use file ```rights_for_ubuntu.sql``` for backend PostgreSQL DB

## How to get started
To reproduce system, please, follow instructions:
1. Install Airflow
2. Create a folder DAGS:
3. Add script ```create_empty_ec2_via_terraform.py``` to the folder
4. Run a script ``` airflow run terraform templated 2018-10-01 ```
