import os
import pandas as pd
from sqlalchemy import create_engine, text

DATA_DIR = "data/raw"
DB_URL = "postgresql://dataflow:dataflow@localhost:5432/dataflow"

engine = create_engine(DB_URL)

with engine.connect() as conn:
    conn.execute(text("CREATE SCHEMA IF NOT EXISTS raw"))
    conn.commit()

for filename in os.listdir(DATA_DIR):
    if not filename.endswith(".csv"):
        continue
    table_name = filename.replace("olist_", "").replace("_dataset.csv", "").replace(".csv", "")
    path = os.path.join(DATA_DIR, filename)
    df = pd.read_csv(path)
    df.to_sql(table_name, engine, schema="raw", if_exists="replace", index=False)
    print(f"Loaded {filename} -> raw.{table_name} ({len(df)} rows)")