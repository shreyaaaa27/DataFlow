import duckdb
import pandas as pd
from sqlalchemy import create_engine

pg_engine = create_engine("postgresql://dataflow:dataflow@localhost:5432/dataflow")
duck_conn = duckdb.connect("dataflow_marts.duckdb")

mart_tables = ["fct_orders", "dim_customers", "dim_products"]

for table in mart_tables:
    df = pd.read_sql(f"SELECT * FROM {table}", pg_engine)
    duck_conn.execute(f"CREATE OR REPLACE TABLE {table} AS SELECT * FROM df")
    print(f"Exported {len(df)} rows to DuckDB table: {table}")

duck_conn.close()