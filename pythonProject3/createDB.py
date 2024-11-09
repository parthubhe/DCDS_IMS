import mysql.connector
from faker import Faker
import random

# Initialize the faker object
fake = Faker()

# Connect to MySQL database
conn = mysql.connector.connect(
    host="localhost",  # Replace with your host
    user="root",  # Replace with your MySQL username
    password="P@rthubh3",  # Replace with your MySQL password
    database="inventory_management"  # Replace with your database name
)
cursor = conn.cursor()

# Create tables
cursor.execute('''CREATE TABLE IF NOT EXISTS Brands (
                    bid INT AUTO_INCREMENT PRIMARY KEY,
                    bname VARCHAR(255))''')

cursor.execute('''CREATE TABLE IF NOT EXISTS inv_user (
                    user_id VARCHAR(255) PRIMARY KEY,
                    name VARCHAR(255),
                    password VARCHAR(255),
                    last_login DATETIME,
                    user_type VARCHAR(50))''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Categories (
                    cid INT AUTO_INCREMENT PRIMARY KEY,
                    category_name VARCHAR(255))''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Stores (
                    sid INT AUTO_INCREMENT PRIMARY KEY,
                    sname VARCHAR(255),
                    address VARCHAR(255),
                    mobno VARCHAR(20))''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Products (
                    pid INT AUTO_INCREMENT PRIMARY KEY,
                    cid INT,
                    bid INT,
                    sid INT,
                    pname VARCHAR(255),
                    p_stock INT,
                    price DECIMAL(10, 2),
                    added_date DATE,
                    FOREIGN KEY (cid) REFERENCES Categories(cid),
                    FOREIGN KEY (bid) REFERENCES Brands(bid),
                    FOREIGN KEY (sid) REFERENCES Stores(sid))''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Providers (
                    bid INT,
                    sid INT,
                    discount DECIMAL(5, 2),
                    FOREIGN KEY (bid) REFERENCES Brands(bid),
                    FOREIGN KEY (sid) REFERENCES Stores(sid))''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Customer_cart (
                    cust_id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255),
                    mobno VARCHAR(15))''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Select_product (
                    cust_id INT,
                    pid INT,
                    quantity INT,
                    FOREIGN KEY (cust_id) REFERENCES Customer_cart(cust_id),
                    FOREIGN KEY (pid) REFERENCES Products(pid))''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Transaction (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    total_amount DECIMAL(10, 2),
                    paid DECIMAL(10, 2),
                    due DECIMAL(10, 2),
                    gst DECIMAL(5, 2),
                    discount DECIMAL(5, 2),
                    payment_method VARCHAR(50),
                    cart_id INT,
                    FOREIGN KEY (cart_id) REFERENCES Customer_cart(cust_id))''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Invoice (
                    item_no INT AUTO_INCREMENT PRIMARY KEY,
                    product_name VARCHAR(255),
                    quantity INT,
                    net_price DECIMAL(10, 2),
                    transaction_id INT,
                    FOREIGN KEY (transaction_id) REFERENCES Transaction(id))''')


# Function to populate tables with fake data
def populate_data():
    # Store valid ids for use in foreign keys
    brand_ids = []
    category_ids = []
    store_ids = []
    customer_ids = []
    product_ids = []

    # Insert into Brands and store bid
    for _ in range(10):
        cursor.execute("INSERT INTO Brands (bname) VALUES (%s)", (fake.company(),))
        brand_ids.append(cursor.lastrowid)  # Store inserted bid

    # Insert into inv_user
    for _ in range(10):
        cursor.execute(
            "INSERT INTO inv_user (user_id, name, password, last_login, user_type) VALUES (%s, %s, %s, %s, %s)",
            (fake.email(), fake.name(), fake.password(), fake.date_time_this_year(),
             random.choice(['Admin', 'Manager', 'Clerk'])))

    # Insert into Categories and store cid
    categories = ['Electronics', 'Clothing', 'Groceries', 'Furniture', 'Toys']
    for category in categories:
        cursor.execute("INSERT INTO Categories (category_name) VALUES (%s)", (category,))
        category_ids.append(cursor.lastrowid)  # Store inserted cid

    # Insert into Stores and store sid
    for _ in range(5):
        cursor.execute("INSERT INTO Stores (sname, address, mobno) VALUES (%s, %s, %s)",
                       (fake.company(), fake.address(), fake.phone_number()[:15]))
        store_ids.append(cursor.lastrowid)  # Store inserted sid

    # Insert into Products using valid foreign key ids
    # Insert into Products using valid foreign key ids
    for _ in range(1000):  # Increased to insert 1000 products
        cursor.execute('''INSERT INTO Products (cid, bid, sid, pname, p_stock, price, added_date)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)''',
                       (random.choice(category_ids), random.choice(brand_ids), random.choice(store_ids),
                        fake.word(), random.randint(10, 100), random.uniform(10, 500), fake.date()))
        product_ids.append(cursor.lastrowid)

        # Insert into Providers using valid foreign key ids
    for _ in range(10):
        cursor.execute("INSERT INTO Providers (bid, sid, discount) VALUES (%s, %s, %s)",
                       (random.choice(brand_ids), random.choice(store_ids), random.uniform(5, 25)))

    # Insert into Customer_cart and store cust_id
    for _ in range(10):
        cursor.execute("INSERT INTO Customer_cart (name, mobno) VALUES (%s, %s)",
                       (fake.name(), fake.phone_number()[:15]))
        customer_ids.append(cursor.lastrowid)  # Store inserted cust_id

    # Insert into Select_product using valid cust_id and pid
    for _ in range(15):
        cursor.execute("INSERT INTO Select_product (cust_id, pid, quantity) VALUES (%s, %s, %s)",
                       (random.choice(customer_ids), random.choice(product_ids), random.randint(1, 10)))

    # Insert into Transaction using valid cart_id
    for _ in range(10):
        total = random.uniform(50, 1000)
        paid = total - random.uniform(0, total)
        cursor.execute('''INSERT INTO Transaction (total_amount, paid, due, gst, discount, payment_method, cart_id)
                          VALUES (%s, %s, %s, %s, %s, %s, %s)''',
                       (total, paid, total - paid, random.uniform(5, 18), random.uniform(5, 20),
                        random.choice(['Cash', 'Card']), random.choice(customer_ids)))

    # Insert into Invoice using valid transaction_id
    for _ in range(20):
        cursor.execute('''INSERT INTO Invoice (product_name, quantity, net_price, transaction_id)
                          VALUES (%s, %s, %s, %s)''',
                       (fake.word(), random.randint(1, 10), random.uniform(10, 100), random.randint(1, 10)))

    conn.commit()


# Populate the tables with fake data
populate_data()

# Close the connection
cursor.close()
conn.close()
