import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql://dataflow:dataflow@localhost:5432/dataflow")

tables = ["orders", "customers", "order_items", "order_payments", "order_reviews", "products", "sellers"]

for table in tables:
    df = pd.read_sql(f"SELECT * FROM raw.{table}", engine)
    print(f"\n--- {table} ({len(df)} rows) ---")
    print("Nulls per column:\n", df.isnull().sum()[df.isnull().sum() > 0])
    print("Duplicate rows:", df.duplicated().sum())

# Cardinality verification for order_reviews
print("\n--- Relationship Verification ---")
df_reviews = pd.read_sql("SELECT order_id FROM raw.order_reviews", engine)
dup_reviews = df_reviews["order_id"].duplicated().sum()
print(f"order_reviews duplicate order_ids: {dup_reviews}")
if dup_reviews > 0:
    print("Cardinality confirmed: orders -> order_reviews is 1-to-Many (1:N)")
else:
    print("Cardinality confirmed: orders -> order_reviews is 1-to-1 (1:1)")