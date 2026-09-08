from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine, text

DB_URL = "postgresql://dataflow:dataflow@postgres:5432/dataflow"
DATA_DIR = "/opt/airflow/data/raw"

TABLES = {
    "orders": "olist_orders_dataset.csv",
    "customers": "olist_customers_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "order_payments": "olist_order_payments_dataset.csv",
    "order_reviews": "olist_order_reviews_dataset.csv",
    "products": "olist_products_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
}


def load_table(table_name: str, filename: str):
    engine = create_engine(DB_URL)

    with engine.begin() as conn:  # engine.begin() auto-commits on success, auto-rolls-back on error
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS raw"))

    df = pd.read_csv(f"{DATA_DIR}/{filename}")
    df.to_sql(table_name, engine, schema="raw", if_exists="replace", index=False)
    print(f"Loaded {len(df)} rows into raw.{table_name}")


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