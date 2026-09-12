select
    o.order_id,
    o.customer_id,
    o.order_status,
    o.purchase_ts,
    o.delivered_ts,
    o.estimated_delivery_ts,
    case
        when o.delivered_ts is not null and o.estimated_delivery_ts is not null
        then (o.delivered_ts::date - o.estimated_delivery_ts::date)
        else null
    end as delivery_delay_days,
    items.num_items,
    items.items_total,
    items.freight_total,
    payments.payment_total,
    payments.num_payment_installments
from {{ ref('stg_orders') }} o
left join {{ ref('int_order_items_agg') }} items on o.order_id = items.order_id
left join {{ ref('int_order_payments_agg') }} payments on o.order_id = payments.order_id