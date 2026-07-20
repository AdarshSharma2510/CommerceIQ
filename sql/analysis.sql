-- ==========================================================
-- EXECUTIVE KPIs
-- ==========================================================

-- Total Revenue
SELECT
    ROUND(SUM(total_order_value), 2) AS total_revenue
FROM ecommerce_data;


-- Total Orders
SELECT
    COUNT(DISTINCT order_id) AS total_orders
FROM ecommerce_data;


-- Average Order Value
SELECT
    ROUND(AVG(total_order_value), 2) AS average_order_value
FROM ecommerce_data;


-- Average Review Score
SELECT
    ROUND(AVG(review_score), 2) AS average_review
FROM ecommerce_data;


-- Delayed Order Percentage
SELECT
    ROUND(
        100.0 * SUM(is_delayed) / COUNT(*),
        2
    ) AS delayed_percentage
FROM ecommerce_data;



-- ==========================================================
-- SALES ANALYSIS
-- ==========================================================

-- Monthly Revenue
SELECT
    purchase_month,
    ROUND(SUM(total_order_value),2) AS revenue
FROM ecommerce_data
GROUP BY purchase_month
ORDER BY purchase_month;


-- Monthly Orders
SELECT
    purchase_month,
    COUNT(*) AS orders
FROM ecommerce_data
GROUP BY purchase_month
ORDER BY purchase_month;


-- Revenue by Quarter
SELECT
    purchase_quarter,
    ROUND(SUM(total_order_value),2) AS revenue
FROM ecommerce_data
GROUP BY purchase_quarter
ORDER BY purchase_quarter;


-- Highest Revenue Categories
SELECT
    main_category,
    ROUND(SUM(total_order_value),2) AS revenue
FROM ecommerce_data
GROUP BY main_category
ORDER BY revenue DESC
LIMIT 10;


-- Average Basket Size
SELECT
    ROUND(AVG(total_items),2) AS average_items
FROM ecommerce_data;


-- ==========================================================
-- CUSTOMER ANALYSIS
-- ==========================================================

-- Business Question:
-- Which customers have spent the most?

SELECT
    customer_unique_id,
    ROUND(SUM(total_order_value), 2) AS total_spent
FROM ecommerce_data
GROUP BY customer_unique_id
ORDER BY total_spent DESC
LIMIT 10;


-- Business Question:
-- Which customers have placed the most orders?

SELECT
    customer_unique_id,
    COUNT(order_id) AS total_orders
FROM ecommerce_data
GROUP BY customer_unique_id
ORDER BY total_orders DESC
LIMIT 10;


-- Business Question:
-- Which payment methods are used the most?

SELECT
    payment_type,
    COUNT(*) AS total_orders
FROM ecommerce_data
GROUP BY payment_type
ORDER BY total_orders DESC;


-- Business Question:
-- Which payment methods generate the highest revenue?

SELECT
    payment_type,
    ROUND(SUM(total_order_value), 2) AS revenue
FROM ecommerce_data
GROUP BY payment_type
ORDER BY revenue DESC;


-- ==========================================================
-- LOGISTICS ANALYSIS
-- ==========================================================

-- Business Question:
-- What is the average delivery time?

SELECT
    ROUND(AVG(delivery_days), 2) AS average_delivery_days
FROM ecommerce_data;


-- Business Question:
-- Which order statuses occur most frequently?

SELECT
    order_status,
    COUNT(*) AS total_orders
FROM ecommerce_data
GROUP BY order_status
ORDER BY total_orders DESC;


-- Business Question:
-- Which months have the highest delivery delays?

SELECT
    purchase_month,
    ROUND(AVG(delivery_delay), 2) AS average_delay
FROM ecommerce_data
GROUP BY purchase_month
ORDER BY average_delay DESC;


-- ==========================================================
-- ADVANCED SQL
-- ==========================================================

-- Business Question:
-- Rank product categories by total revenue.

SELECT
    main_category,
    ROUND(SUM(total_order_value), 2) AS revenue,
    DENSE_RANK() OVER (
        ORDER BY SUM(total_order_value) DESC
    ) AS revenue_rank
FROM ecommerce_data
GROUP BY main_category;


-- Business Question:
-- Calculate cumulative monthly revenue.

SELECT
    purchase_month,
    ROUND(SUM(total_order_value), 2) AS revenue,
    ROUND(
        SUM(SUM(total_order_value))
        OVER (
            ORDER BY purchase_month
        ),
        2
    ) AS cumulative_revenue
FROM ecommerce_data
GROUP BY purchase_month
ORDER BY purchase_month;


-- Business Question:
-- Rank customers by total spending.

SELECT
    customer_unique_id,
    ROUND(SUM(total_order_value), 2) AS total_spent,
    RANK() OVER (
        ORDER BY SUM(total_order_value) DESC
    ) AS spending_rank
FROM ecommerce_data
GROUP BY customer_unique_id
LIMIT 20;


-- Business Question:
-- Find the top-selling category each month.

WITH category_sales AS (

    SELECT
        purchase_month,
        main_category,
        SUM(total_order_value) AS revenue

    FROM ecommerce_data

    GROUP BY
        purchase_month,
        main_category

),

ranked_categories AS (

    SELECT
        purchase_month,
        main_category,
        revenue,
        ROW_NUMBER() OVER (
            PARTITION BY purchase_month
            ORDER BY revenue DESC
        ) AS rank_number

    FROM category_sales

)

SELECT
    purchase_month,
    main_category,
    ROUND(revenue, 2) AS revenue
FROM ranked_categories
WHERE rank_number = 1
ORDER BY purchase_month;


-- Business Question:
-- What is the monthly average order value?

SELECT
    purchase_month,
    ROUND(AVG(total_order_value), 2) AS average_order_value
FROM ecommerce_data
GROUP BY purchase_month
ORDER BY purchase_month;


-- Business Question:
-- Which product categories have the highest average review score?

SELECT
    main_category,
    ROUND(AVG(review_score), 2) AS average_review
FROM ecommerce_data
GROUP BY main_category
HAVING COUNT(*) >= 100
ORDER BY average_review DESC;


-- Business Question:
-- Which weekdays receive the highest number of orders?

SELECT
    purchase_weekday,
    COUNT(*) AS total_orders
FROM ecommerce_data
GROUP BY purchase_weekday
ORDER BY total_orders DESC;