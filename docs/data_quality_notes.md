# Data Quality & Profiling Notes (Olist E-Commerce Dataset)

## Overview
- **Source Database**: `dataflow` (Schema: `raw`)
- **Total Tables**: 7
- **Duplicate Rows**: 0 across all tables.

---

## Findings & Handling Strategies

### 1. `orders` Table
- **Total Rows**: 99,441
- **Null Values**:
  - `order_approved_at`: 160 missing
  - `order_delivered_carrier_date`: 1,783 missing
  - `order_delivered_customer_date`: 2,965 missing

#### Business Context & Data Note
* **Real Business Fact (Not Missing Data to Fix)**: These missing timestamps reflect order lifecycle states rather than bad data ingestion. For instance:
  - Canceled or unavailable orders never get shipped or delivered.
  - Pending orders haven't reached carrier handoff or delivery yet.
* **Impact**: Do **not** drop these rows or impute them with mean/mode dates. Filtering them out would inadvertently drop valid non-delivered orders, corrupting order status and cancellation metrics.

---

### 2. `order_reviews` Table
- **Total Rows**: 99,224
- **Null Values**:
  - `review_comment_title`: 87,656 missing (~88.3%)
  - `review_comment_message`: 58,247 missing (~58.7%)

#### Business Context & Data Note
* **Expected Customer Behavior**: Providing text feedback is optional. Most customers submit a score (1–5 stars) without typing a written review or title.
* **Impact**:
  - Review score analysis (NPS, average rating) is unaffected as core ratings remain intact.
  - For NLP/sentiment analysis, treat missing review text as an empty string (`""`) or filter down exclusively to rows where text is present.

---

### 3. `products` Table
- **Total Rows**: 32,951
- **Null Values**:
  - `product_category_name`, `product_name_lenght`, `product_description_lenght`, `product_photos_qty`: 610 missing (~1.85%)
  - `product_weight_g`, `product_length_cm`, `product_height_cm`, `product_width_cm`: 2 missing

#### Business Context & Data Note
* **Uncategorized/Incomplete Products**: 610 products lack category mappings and metadata.
* **Impact**:
  - Fill missing `product_category_name` with `'unknown'` or `'other'` during ETL joins to avoid dropping sales volume in category-level reports.
  - Measure dimension nulls (2 rows) can be safely ignored or ignored during weight/freight calculations.

---

### 4. Fully Complete Tables (`0` Nulls, `0` Duplicates)
The following primary/reference entities have complete integrity and require no null handling:

| Table | Total Rows | Data Quality Status |
| :--- | :--- | :--- |
| `customers` | 99,441 | **100% Complete** |
| `order_items` | 112,650 | **100% Complete** |
| `order_payments` | 103,886 | **100% Complete** |
| `sellers` | 3,095 | **100% Complete** |

---

## Key Takeaways for Downstream Pipeline / Transformations

1. **Outer Joins vs. Inner Joins**:
   - Use `LEFT JOIN` when building analytics models around `orders` and `order_reviews` to prevent losing non-reviewed or non-delivered orders.
2. **Date Filters**:
   - When calculating delivery lead times (e.g., `order_delivered_customer_date - order_purchase_timestamp`), explicitly filter for `order_status = 'delivered'` to avoid operating on `NULL` dates.
3. **Product Category Mapping**:
   - Apply explicit `COALESCE(product_category_name, 'unknown')` during transformations.

---

## Schema Drift Test & Ingestion Limitations

### Test Result
Ran `tests/test_profiling_output.py` simulating an upstream CSV schema change (`new_column` added).
- **Observed Behavior**: Pandas successfully loaded the unexpected column into the DataFrame schema without raising an error or warning:
  `['order_id', ..., 'order_estimated_delivery_date', 'new_column']`

### Data Quality & Pipeline Impact
Using `pandas.DataFrame.to_sql(..., if_exists="replace")` presents significant risks in production pipelines:
1. **Uncontrolled Schema Changes**: New columns silently bypass table contracts.
2. **Silent Column Loss**: If an upstream source drops a required column, `if_exists="replace"` will drop and recreate the table without it, silently corrupting historical database schemas.
3. **Downstream Pipeline Breakage**: Missing columns will cause downstream dbt transformations and reporting queries to fail at runtime.

### Recommended Production Pattern
- Avoid `if_exists="replace"`.
- Use pre-defined database DDL schemas combined with `if_exists="append"`.
- Implement explicit schema contract checks prior to ingestion (e.g., using **Great Expectations** or **Pandera**) to catch added or missing columns before database insertion.