select
    order_id,
    count(*) as num_items,
    sum(price) as items_total,
    sum(freight_value) as freight_total,
    count(distinct seller_id) as num_distinct_sellers
from {{ ref('stg_order_items') }}
group by order_id