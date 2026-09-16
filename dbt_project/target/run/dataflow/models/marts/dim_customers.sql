
  
    

  create  table "dataflow"."public"."dim_customers__dbt_tmp"
  
  
    as
  
  (
    select
    customer_id,
    customer_city,
    customer_state,
    customer_zip_code_prefix
from "dataflow"."raw"."customers"
  );
  