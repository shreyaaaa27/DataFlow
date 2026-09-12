select
    f.purchase_month,
    c.customer_state,
    sum(f.payment_total) as total_revenue,
    count(distinct f.order_id) as num_orders,
    avg(f.delivery_delay_days) as avg_delivery_delay
from {{ ref('fct_orders') }} f
join {{ ref('dim_customers') }} c on f.customer_id = c.customer_id
group by 1, 2
order by 1, 2