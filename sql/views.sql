-- Average home price and property count by city for affordability analysis
CREATE VIEW avg_price_by_city AS
SELECT city, AVG(price) AS avg_price, COUNT(*) AS property_count
FROM properties
GROUP BY city;

-- Typical home features by city (beds, baths, price per sqft) to understand what you get for your money
CREATE VIEW city_property_features AS
SELECT city, AVG(price_per_sqft) AS avg_price_per_sqft, AVG(bed) AS avg_bedrooms, AVG(bath) AS avg_bathrooms
FROM properties
GROUP BY city;

-- Distribution of Budget/Mid-Range/Luxury homes by city to understand market composition
CREATE VIEW price_category_by_city AS
SELECT city, price_category, COUNT(*) AS property_count
FROM properties
GROUP BY city, price_category;

-- Market activity by city showing for sale vs sold properties to gauge competitiveness
CREATE VIEW status_by_city AS
SELECT city, status, COUNT(*) AS property_count
FROM properties
GROUP BY city, status;

-- Sales trend over last few years by month due to seasonality
CREATE VIEW sales_by_month_year AS
SELECT city, 
strftime('%Y-%m', prev_sold_date) AS sale_month,
avg(price) AS avg_price,
count(*) AS sales_count
FROM properties
WHERE prev_sold_date IS NOT NULL
GROUP BY city, sale_month;