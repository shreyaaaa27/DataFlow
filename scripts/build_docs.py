import great_expectations as gx

context = gx.get_context(mode="file", project_root_dir=".")
context.build_data_docs()
print("Data docs built successfully.")
