use customer_analysis;
SHOW TABLES;
SELECT COUNT(*) FROM customer_shopping;

#1. what is total amount spent by male and female customer
SELECT `Gender`,sum(`Purchase Amount (USD)`) as total_amount
FROM customer_shopping
Group by Gender;
-- Male	157890
-- Female	75191

#2.Which customer used a discount but still purchased more than average amount
SELECT COUNT(`Customer ID`),avg(`Purchase Amount (USD)`) as avg_amount
FROM customer_shopping
WHERE `Discount Applied`="Yes" and `Purchase Amount (USD)` >=(
SELECT avg(`Purchase Amount (USD)`) as avg_amount
FROM customer_shopping
);
-- count of customers 839	#average amount79.7878

#3.what are the top 5 products  whose review is greater than average rating
SELECT (`Item Purchased`),AVG(`Review Rating`) as avg_rating
FROM customer_shopping
GROUP BY `Item Purchased`
ORDER BY avg_rating DESC limit 5;
-- Gloves	3.8627737226277383
-- Sandals	3.8446540880503144
-- Boots	3.818881118881119
-- Hat	3.801307189542483
-- Skirt	3.7853503184713366

#4.compare avergae purchase amounts between standard and express shipping
SELECT AVG(`Purchase Amount (USD)`),`Shipping Type`
FROM customer_shopping
Group by `Shipping Type`;
-- 60.4752	Express
-- 60.4104	Free Shipping
-- 58.6312	Next Day Air
-- 58.4602	Standard
-- 60.7337	2-Day Shipping
-- 59.8938	Store Pickup
#there's no much difference between express and free shipping

#5.Do suscribed customers spend more comapre between suscribed and unsuscribed customers
SELECT AVG(`Purchase Amount (USD)`),`Subscription status`,sum(`Purchase Amount (USD)`)
FROM customer_shopping
GROUP BY `Subscription status`;
-- 59.4919	Yes 62645
-- 59.8651	No 170436
#people those who have not subscribed are buying more

#6.Which 5 products have the highest percentage of purchase with discount applie
SELECT 
    `Item Purchased`,
    ROUND(
        SUM(CASE WHEN `Discount Applied` = 'Yes' THEN 1 ELSE 0 END) 
        / COUNT(*) * 100, 
        2
    ) AS discount_rate
FROM customer_shopping
GROUP BY `Item Purchased`
ORDER BY discount_rate DESC
LIMIT 5;

#7.Segment the customers based on their previous purchased as new returnung loyal and show their count also
SELECT 
    CASE
        WHEN `Previous Purchases` > 30 THEN 'Loyal'
        WHEN `Previous Purchases` > 20 THEN 'Returning'
        WHEN `Previous Purchases` > 10 THEN 'New Customer'
        ELSE 'Invalid'
    END AS customer_loyalty_status,
    COUNT(`Customer ID`) AS total_customers
FROM customer_shopping
GROUP BY customer_loyalty_status;

#8.What is top most products purchased in each category
SELECT 
    Category,
    `Item Purchased`,
    COUNT(*) AS item_count
FROM customer_shopping
GROUP BY Category, `Item Purchased`
ORDER BY Category, item_count DESC;

#9.Are customers who are repeat buyers from subscriber or not
SELECT `Subscription Status`,COUNT(`Previous Purchases`)
FROM customer_shopping
Where `Previous Purchases`>5
GROUP BY `Subscription Status`;

show databases;

