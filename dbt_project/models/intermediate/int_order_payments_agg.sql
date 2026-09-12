select
    order_id,
    sum(payment_value) as payment_total,
    count(*) as num_payment_installments,
    array_agg(distinct payment_type) as payment_types
from {{ ref('stg_order_payments') }}
group by order_id