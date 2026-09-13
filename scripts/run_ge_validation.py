import great_expectations as gx

context = gx.get_context(mode="file", project_root_dir=".")

datasource = context.data_sources.get("dataflow_postgres")
asset = datasource.get_asset("fct_orders")
batch_definition = asset.get_batch_definition("fct_orders_batch")
suite = context.suites.get("fct_orders_suite")

validation_definition = gx.ValidationDefinition(
    data=batch_definition,
    suite=suite,
    name="fct_orders_validation",
)
validation_definition = context.validation_definitions.add_or_update(validation_definition)

checkpoint = gx.Checkpoint(
    name="fct_orders_checkpoint",
    validation_definitions=[validation_definition],
)
checkpoint = context.checkpoints.add_or_update(checkpoint)

result = checkpoint.run()

if not result.success:
    for validation_result in result.run_results.values():
        for res in validation_result.results:
            if not res.success:
                print("FAILED:", res.expectation_config.type)
                print("  Column:", res.expectation_config.kwargs.get("column"))
                print("  Details:", res.result)
    raise Exception("Data quality validation failed")

print("All expectations passed.")