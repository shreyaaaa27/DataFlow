from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime
from extract_load_dag import load_table, TABLES


def run_ge_validation():
    import subprocess
    result = subprocess.run(
        ["python3", "/opt/airflow/scripts/run_ge_validation.py"],
        capture_output=True, text=True,
    )
    print(result.stdout)
    if result.returncode != 0:
        raise Exception(f"Data quality validation failed:\n{result.stderr}")


with DAG(
    dag_id="dataflow_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    default_args={"retries": 2, "retry_delay": 30},
) as dag:

    extract_tasks = [
        PythonOperator(
            task_id=f"load_{table_name}",
            python_callable=load_table,
            op_kwargs={"table_name": table_name, "filename": filename},
        )
        for table_name, filename in TABLES.items()
    ]

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command="cd /opt/airflow/dbt_project && dbt run",
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command="cd /opt/airflow/dbt_project && dbt test",
    )

    data_quality_check = PythonOperator(
        task_id="great_expectations_validation",
        python_callable=run_ge_validation,
    )

    extract_tasks >> dbt_run >> dbt_test >> data_quality_check