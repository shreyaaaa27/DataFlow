import great_expectations as gx

context = gx.get_context(
    mode="file",
    project_root_dir="."
)

datasource = context.data_sources.add_or_update_postgres(
    name="dataflow_postgres",
    connection_string="postgresql+psycopg2://dataflow:dataflow@localhost:5432/dataflow",
)

try:
    asset = datasource.add_table_asset(
        name="fct_orders",
        table_name="fct_orders",
        schema_name="public",
    )
except Exception:
    asset = datasource.get_asset("fct_orders")

# 3. Define the whole table as one batch
batch_definition = asset.add_batch_definition_whole_table(
    name="fct_orders_batch"
)

# 4. Create the expectation suite
suite = gx.ExpectationSuite(name="fct_orders_suite")
suite = context.suites.add_or_update(suite)

# Clear any expectations left over from previous runs before re-adding
suite.expectations = []
suite.save()

# 5. Structural expectations

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        column="order_id"
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        column="order_id"
    )
)

# 6. Business-rule expectations

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        column="delivery_delay_days",
        min_value=-60,
        max_value=60,
        mostly=0.99,  # allow up to 1% of rows to fall outside this range
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        column="order_status",
        value_set=[
            "delivered",
            "shipped",
            "canceled",
            "processing",
            "invoiced",
            "created",
            "approved",
            "unavailable"
        ]
    )
)


print("fct_orders_suite created successfully!")