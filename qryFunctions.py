import mysql.connector
from mysql.connector import Error
import matplotlib.pyplot as plt
import io
import base64
from datetime import datetime

# Database connection function
def create_connection():
    """Creates and returns a connection to the MySQL database."""
    try:
        connection = mysql.connector.connect(
            host="localhost",  # Replace with your host
            user="root",  # Replace with your MySQL username
            password="encrypt256*",  # Replace with your MySQL password
            database="inventory_management"  # Replace with your database name
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None


# Function to insert data into the Products table
def insert_product(cid, bid, sid, pname, p_stock, price, added_date):
    """Inserts a new product into the Products table."""
    connection = create_connection()
    cursor = connection.cursor()
    query = """
    INSERT INTO Products (cid, bid, sid, pname, p_stock, price, added_date)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    values = (cid, bid, sid, pname, p_stock, price, added_date)

    try:
        cursor.execute(query, values)
        connection.commit()
        print("Product inserted successfully")
    except Error as e:
        print(f"Error inserting product: {e}")
    finally:
        cursor.close()
        connection.close()


# Function to read products from the Products table
def read_products():
    """Reads and returns all products from the Products table."""
    connection = create_connection()
    cursor = connection.cursor()
    query = "SELECT * FROM Products"

    try:
        cursor.execute(query)
        results = cursor.fetchall()
        return results
    except Error as e:
        print(f"Error reading products: {e}")
        return []
    finally:
        cursor.close()
        connection.close()


# Function to update a product in the Products table
def update_product(pid, pname=None, p_stock=None, price=None):
    """Updates product details (name, stock, price) in the Products table."""
    connection = create_connection()
    cursor = connection.cursor()

    # Building the dynamic query based on which values are provided
    query = "UPDATE Products SET "
    updates = []
    values = []

    if pname is not None:
        updates.append("pname = %s")
        values.append(pname)

    if p_stock is not None:
        updates.append("p_stock = %s")
        values.append(p_stock)

    if price is not None:
        updates.append("price = %s")
        values.append(price)

    query += ", ".join(updates) + " WHERE pid = %s"
    values.append(pid)

    try:
        cursor.execute(query, values)
        connection.commit()
        print("Product updated successfully")
    except Error as e:
        print(f"Error updating product: {e}")
    finally:
        cursor.close()
        connection.close()


# Function to delete a product from the Products table
def delete_product(pid):
    """Deletes a product from the Products table based on product ID (pid)."""
    connection = create_connection()
    cursor = connection.cursor()
    query = "DELETE FROM Products WHERE pid = %s"

    try:
        cursor.execute(query, (pid,))
        connection.commit()
        print("Product deleted successfully")
    except Error as e:
        print(f"Error deleting product: {e}")
    finally:
        cursor.close()
        connection.close()


# Function to increment the stock of a product
def increment_stock(pid):
    """Increases the stock of a product by 1."""
    connection = create_connection()
    cursor = connection.cursor()
    query = "UPDATE Products SET p_stock = p_stock + 1 WHERE pid = %s"

    try:
        cursor.execute(query, (pid,))
        connection.commit()
        print("Product stock incremented successfully")
    except Error as e:
        print(f"Error incrementing stock: {e}")
    finally:
        cursor.close()
        connection.close()


# Function to decrement the stock of a product
def decrement_stock(pid):
    """Decreases the stock of a product by 1 (cannot go below 0)."""
    connection = create_connection()
    cursor = connection.cursor()
    query = "UPDATE Products SET p_stock = p_stock - 1 WHERE pid = %s AND p_stock > 0"

    try:
        cursor.execute(query, (pid,))
        connection.commit()
        print("Product stock decremented successfully")
    except Error as e:
        print(f"Error decrementing stock: {e}")
    finally:
        cursor.close()
        connection.close()


# Function to get restock notifications
def get_restock_notifications():
    """Fetches all restock notifications from the database."""
    connection = create_connection()
    cursor = connection.cursor()
    query = "SELECT * FROM RestockNotifications ORDER BY notification_date DESC"

    try:
        cursor.execute(query)
        notifications = cursor.fetchall()
        return notifications
    except Error as e:
        print(f"Error fetching restock notifications: {e}")
        return []
    finally:
        cursor.close()
        connection.close()





# Function to create a new order
def create_order(customer_id, status, total_amount):
    connection = create_connection()
    cursor = connection.cursor()
    query = """
    INSERT INTO Orders (customer_id, status, total_amount)
    VALUES (%s, %s, %s)
    """
    try:
        cursor.execute(query, (customer_id, status, total_amount))
        connection.commit()
        return cursor.lastrowid  # Return the new order ID
    except Error as e:
        print(f"Error creating order: {e}")
        return None
    finally:
        cursor.close()
        connection.close()
# Function to track orders and returns
def get_orders():
    connection = create_connection()
    cursor = connection.cursor()
    query = "SELECT * FROM Orders"

    try:
        cursor.execute(query)
        return cursor.fetchall()
    except Error as e:
        print(f"Error fetching orders: {e}")
        return []
    finally:
        cursor.close()
        connection.close()







# Function to generate a report of product stock and sales

# Function to generate a report of product stock and sales
def generate_report():
    connection = create_connection()
    cursor = connection.cursor()

    try:
        # Fetch data for different reports
        cursor.execute("""
            SELECT p.pname, SUM(p.p_stock) AS total_stock, SUM(p.price) AS total_price
            FROM Products p
            GROUP BY p.pid, p.pname LIMIT 25
        """)
        product_data = cursor.fetchall()

        cursor.execute("""
            SELECT DATE(o.order_date), SUM(o.total_amount) AS total_sales
            FROM Orders o
            GROUP BY DATE(o.order_date)
        """)
        sales_data = cursor.fetchall()

        cursor.execute("""
            SELECT status, COUNT(*) AS order_count
            FROM Orders
            GROUP BY status
        """)
        order_status_data = cursor.fetchall()

        # Close cursor and connection
        cursor.close()
        connection.close()

        # Prepare data for plots
        product_names = [row[0] for row in product_data]
        total_stocks = [row[1] for row in product_data]
        total_prices = [row[2] for row in product_data]

        # Use the corrected date extraction
        sales_dates = [row[0] for row in sales_data]  # Directly use date objects
        total_sales = [row[1] for row in sales_data]

        statuses = [row[0] for row in order_status_data]
        status_counts = [row[1] for row in order_status_data]

        # Plotting and encoding graphs
        graphs = {}

        # 1. Bar Chart for Stock Levels
        plt.figure(figsize=(8, 5))
        plt.bar(product_names, total_stocks, color='blue')
        plt.xlabel('Product Name')
        plt.ylabel('Total Stock')
        plt.title('Stock Level by Product')
        plt.xticks(rotation=45, ha='right')
        img_stock = io.BytesIO()
        plt.savefig(img_stock, format='png')
        img_stock.seek(0)
        graphs['stock_levels'] = base64.b64encode(img_stock.getvalue()).decode('utf8')

        # 2. Line Chart for Sales Trend Over Time
        plt.figure(figsize=(8, 5))
        plt.plot(sales_dates, total_sales, color='green', marker='o')
        plt.xlabel('Date')
        plt.ylabel('Total Sales')
        plt.title('Sales Trend Over Time')
        plt.xticks(rotation=45)
        img_sales = io.BytesIO()
        plt.savefig(img_sales, format='png')
        img_sales.seek(0)
        graphs['sales_trend'] = base64.b64encode(img_sales.getvalue()).decode('utf8')

        # 3. Pie Chart for Order Status Distribution
        plt.figure(figsize=(6, 6))
        plt.pie(status_counts, labels=statuses, autopct='%1.1f%%', startangle=140)
        plt.title('Order Status Distribution')
        img_status = io.BytesIO()
        plt.savefig(img_status, format='png')
        img_status.seek(0)
        graphs['order_status'] = base64.b64encode(img_status.getvalue()).decode('utf8')

        return graphs  # Returning multiple base64-encoded images

    except Error as e:
        print(f"Error generating report: {e}")
        return None
