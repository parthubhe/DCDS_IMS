use inventory_management;
CREATE TABLE RestockNotifications (
    notification_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT,
    product_name VARCHAR(255),
    message VARCHAR(255),
    notification_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES Products(pid)
);


DELIMITER //

CREATE TRIGGER check_stock
BEFORE UPDATE ON Products
FOR EACH ROW
BEGIN
    -- Check if the new stock (after update) is less than 50
    IF NEW.p_stock < 50 AND OLD.p_stock >= 50 THEN
        -- Insert a message into the RestockNotifications table
        INSERT INTO RestockNotifications (product_id, product_name, message)
        VALUES (NEW.pid, NEW.pname, CONCAT('Restock needed for ', NEW.pname, '. Stock is below 50.'));
    END IF;
END //

DELIMITER ;


 
CREATE TABLE Orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50),
    total_amount DECIMAL(10, 2),
    FOREIGN KEY (customer_id) REFERENCES Customer_cart(cust_id)
);

CREATE TABLE OrderItems (
    order_item_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    product_id INT,
    quantity INT,
    price DECIMAL(10, 2),
    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
    FOREIGN KEY (product_id) REFERENCES Products(pid)
);
 

-- Query to find top-selling products
SELECT p.pname, SUM(oi.quantity) AS total_sold
FROM OrderItems oi
JOIN Products p ON oi.product_id = p.pid
GROUP BY p.pname
ORDER BY total_sold DESC
LIMIT 10;

-- on cascade automatically deletes the rferenced foreign keys in the given tables
 ALTER TABLE RestockNotifications
DROP FOREIGN KEY restocknotifications_ibfk_1;

ALTER TABLE RestockNotifications
ADD CONSTRAINT restocknotifications_ibfk_1
FOREIGN KEY (product_id) REFERENCES Products(pid) ON DELETE CASCADE;

