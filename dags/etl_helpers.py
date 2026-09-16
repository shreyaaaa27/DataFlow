import os
import pandas as pd
from sqlalchemy import create_engine, text, inspect

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

    with engine.begin() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS raw"))

    df = pd.read_csv(f"{DATA_DIR}/{filename}")

    inspector = inspect(engine)
    table_exists = inspector.has_table(table_name, schema="raw")

    if table_exists:
        # Table (and any dbt views built on it) already exist — clear rows instead of dropping
        with engine.begin() as conn:
            conn.execute(text(f'TRUNCATE TABLE raw."{table_name}"'))
        df.to_sql(table_name, engine, schema="raw", if_exists="append", index=False)
    else:
        # First run ever — safe to create fresh
        df.to_sql(table_name, engine, schema="raw", if_exists="replace", index=False)

    print(f"Loaded {len(df)} rows into raw.{table_name}")