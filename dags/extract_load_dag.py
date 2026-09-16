from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from etl_helpers import load_table, TABLES

with DAG(
    dag_id="extract_load_raw",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    default_args={"retries": 2, "retry_delay": 30},
) as dag:
    for table_name, filename in TABLES.items():
        PythonOperator(
            task_id=f"load_{table_name}",
            python_callable=load_table,
            op_kwargs={"table_name": table_name, "filename": filename},
        )