-- Task 1: Users from Brasil registered in 2023
SELECT
  first_name,
  last_name,
  email
FROM `bigquery-public-data.thelook_ecommerce.users`
WHERE country = 'Brasil'
  AND EXTRACT(YEAR FROM created_at) = 2023;


-- Task 2: Product count by category
SELECT
  category,
  COUNT(*) AS product_count
FROM `bigquery-public-data.thelook_ecommerce.products`
GROUP BY category
ORDER BY product_count DESC;


-- Task 3: Shipped orders with customers
SELECT
  o.order_id,
  u.first_name,
  u.last_name,
  o.status
FROM `bigquery-public-data.thelook_ecommerce.orders` o
JOIN `bigquery-public-data.thelook_ecommerce.users` u
  ON o.user_id = u.id
WHERE o.status = 'Shipped';


-- Task 4: Top 10 expensive orders
SELECT
  order_id,
  user_id,
  SUM(sale_price) AS total_sale_price
FROM `bigquery-public-data.thelook_ecommerce.order_items`
GROUP BY order_id, user_id
ORDER BY total_sale_price DESC
LIMIT 10;


-- Task 5: Countries with >500 users
SELECT
  country,
  COUNT(DISTINCT id) AS unique_users
FROM `bigquery-public-data.thelook_ecommerce.users`
GROUP BY country
HAVING COUNT(DISTINCT id) > 500
ORDER BY unique_users DESC;