
  
    

  create  table "dataflow"."public"."dim_products__dbt_tmp"
  
  
    as
  
  (
    select
    p.product_id,
    p.product_category_name,
    t.product_category_name_english,
    p.product_weight_g,
    p.product_photos_qty
from "dataflow"."raw"."products" p
left join "dataflow"."raw"."product_category_name_translation" t
    on p.product_category_name = t.product_category_name
  );
  