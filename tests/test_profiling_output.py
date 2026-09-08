import pandas as pd
df1 = pd.read_csv("data/raw/olist_orders_dataset.csv")
# simulate a "new column added later" scenario
df2 = df1.copy()
df2["new_column"] = "test"
df2.to_csv("/tmp/test_new_col.csv", index=False)
df_reloaded = pd.read_csv("/tmp/test_new_col.csv")
print(df_reloaded.columns)