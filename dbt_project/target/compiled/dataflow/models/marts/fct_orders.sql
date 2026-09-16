select
    order_id,
    customer_id,
    order_status,
    purchase_ts,
    delivered_ts,
    delivery_delay_days,
    num_items,
    items_total,
    freight_total,
    payment_total,
    num_payment_installments,
    date_trunc('month', purchase_ts) as purchase_month
from "dataflow"."public"."int_orders_enriched"