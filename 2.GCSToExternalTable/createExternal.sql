CREATE OR REPLACE EXTERNAL TABLE `ecommerce_dataset.orders_raw_external`
OPTIONS (
  format = 'CSV',
  uris = ['gs://ecomm-bucket/orders_raw.csv'],
  skip_leading_rows = 1
);