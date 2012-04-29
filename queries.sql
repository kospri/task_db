
--SELECT * FROM customer ORDER BY id_customer;
--SELECT * FROM address ORDER BY id_address
--SELECT * FROM orders ORDER BY id_order;

-- Get simple count of records in each table:
SELECT COUNT(customer.id_customer) AS "Customers", 
       COUNT(address.id_address) AS "Addresses",
       COUNT(orders.id_order) AS "Orders"
FROM customer, address, orders;

--How many addresses has each customer:
SELECT customer.id_customer AS "Customer", 
       COUNT(address.id_address) AS "Addresses"
FROM  customer, address
WHERE customer.id_customer = address.key_customer
GROUP BY customer.id_customer;

-- Get full information about customer:
SELECT customer.id_customer AS "Id", customer.firstname AS "Name",
       customer.lastname AS "Surname", customer.email AS "Email",
       address.id_address AS "Address Id", address.address_line1 AS "Line 1",
       COALESCE(address.address_line2,'----') AS "Line 2",
       address.postcode AS "Post code", address.country AS "Country",
       COALESCE(address.region, '----') AS "Region",
       COALESCE(address.city, '----') AS "City"
FROM customer JOIN address ON customer.id_customer = address.key_customer;

-- Get info about order:
SELECT orders.id_order AS "Order Id", orders.key_status AS "Status code",
       CASE WHEN orders.delivered=TRUE THEN 'Yes' ELSE 'No' END AS "Delivered",
       customer.firstname AS "Name", customer.lastname AS "Surname",
       address.address_line1 AS "Address line 1", address.postcode AS "Post code",
       address.country AS "Country"
FROM orders, customer, address
WHERE (orders.key_customer = customer.id_customer) 
  AND (orders.key_address  = address.id_address)
  AND (orders.key_customer = address.key_customer);
