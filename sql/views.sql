-- Average home price and property count by city for affordability analysis
CREATE VIEW avg_price_by_city AS
SELECT city, AVG(price) AS avg_price, COUNT(*) AS property_count
FROM properties
GROUP BY city;

CREATE VIEW 