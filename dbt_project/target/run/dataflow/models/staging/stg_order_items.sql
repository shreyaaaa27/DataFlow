
  create view "dataflow"."public"."stg_order_items__dbt_tmp"
    
    
  as (
    select
    order_id,
    order_item_id,
    product_id,
    seller_id,
    price::numeric as price,
    freight_value::numeric as freight_value
from "dataflow"."raw"."order_items"
  );