This README is designed to reflect your specific **Medallion Architecture** (Bronze $\rightarrow$ Silver $\rightarrow$ Gold) and your updated configuration for the `ecommerce_dataset` in the Montreal region.

---

# E-commerce Data Pipeline (Dataform)

This project manages the ELT (Extract, Load, Transform) pipeline for e-commerce order data within BigQuery using **Dataform Core 3.0.42**.

## 🏗 Architecture: The Medallion Flow

The pipeline follows a tiered data architecture to ensure data quality and traceability:

1.  **Bronze (`orders_bronze`)**: A raw-to-refined copy of the source data. This layer captures the history and original state of every order record.
2.  **Silver (`orders_silver`)**: The "Clean" layer. We apply deduplication logic here to ensure that only the most recent version of an order is preserved.
3.  **Gold (`orders_gold`)**: The "Reporting" layer. Data is aggregated at the customer level to provide high-level business metrics like Lifetime Value (LTV) and order frequency.

---

## ⚙️ Configuration

- **Project ID**: `amiable-hour-315409`
- **Default Dataset**: `ecommerce_dataset`
- **Location**: `northamerica-northeast1` (Montreal)
- **Assertion Dataset**: `ecommerce_dataset_assertions`

---

## 📂 Table Definitions

### 1. Bronze Layer
* **Source**: `ecommerce_dataset.orders_raw`
* **Transformation**: Direct selection of all columns to move data into the managed Dataform workflow.

### 2. Silver Layer
* **Logic**: Uses a `ROW_NUMBER()` window function partitioned by `order_id` and ordered by `order_date DESC`.
* **Goal**: Deduplication. It removes stale records and only keeps the latest update for any given order.

### 3. Gold Layer
* **Logic**: Aggregates metrics (Sum of revenue, Average order value, Count of orders) grouped by `customer_id`.
* **Goal**: Powering BI dashboards and marketing analysis.

---

## 🚀 Getting Started

1.  **Prerequisites**:
    * Ensure the BigQuery dataset `ecommerce_dataset` exists in the `northamerica-northeast1` region.
    * Service account must have `BigQuery Data Editor` and `BigQuery Job User` roles.

2.  **Compilation**:
    Click the **Compile** button in the Dataform UI to build the dependency graph. Ensure the graph shows a linear flow:
    `orders_raw` $\rightarrow$ `orders_bronze` $\rightarrow$ `orders_silver` $\rightarrow$ `orders_gold`.

3.  **Execution**:
    To build the full pipeline, run the tags or execute the Gold table with "Run with Dependencies" selected.

---

## 🛠 Troubleshooting

* **Location Errors**: If you see a "Not found" error in `northamerica-northeast1`, verify that your source `orders_raw` table is located in the same Montreal region. BigQuery cannot perform cross-region joins.
* **Table Not Found**: Ensure you execute the tables in order. `orders_silver` will fail if `orders_bronze` has not been created yet.