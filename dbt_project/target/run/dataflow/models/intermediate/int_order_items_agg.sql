
  create view "dataflow"."public"."int_order_items_agg__dbt_tmp"
    
    
  as (
    select
    order_id,
    count(*) as num_items,
    sum(price) as items_total,
    sum(freight_value) as freight_total,
    count(distinct seller_id) as num_distinct_sellers
from "dataflow"."public"."stg_order_items"
group by order_id
  );