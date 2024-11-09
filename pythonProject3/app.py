from flask import Flask, render_template, request, redirect, url_for
from qryFunctions import (
    insert_product, read_products, update_product, delete_product,
    increment_stock, decrement_stock, get_restock_notifications,
       generate_report,create_order,get_orders
)

app = Flask(__name__)

# Home route (read all products)
@app.route('/')
def index():
    products = read_products()  # Get all products
    notifications = get_restock_notifications()  # Get restock notifications
    return render_template('index.html', products=products, notifications=notifications)

# Route to insert a new product
@app.route('/insert', methods=['POST', 'GET'])
def insert():
    if request.method == 'POST':
        cid = request.form['cid']
        bid = request.form['bid']
        sid = request.form['sid']
        pname = request.form['pname']
        p_stock = request.form['p_stock']
        price = request.form['price']
        added_date = request.form['added_date']

        insert_product(cid, bid, sid, pname, p_stock, price, added_date)
        return redirect(url_for('index'))

    return render_template('insert.html')

# Route to update a product
@app.route('/update/<int:pid>', methods=['POST', 'GET'])
def update(pid):
    if request.method == 'POST':
        pname = request.form['pname']
        p_stock = request.form['p_stock']
        price = request.form['price']

        update_product(pid, pname=pname, p_stock=p_stock, price=price)
        return redirect(url_for('index'))

    products = read_products()
    product = next((p for p in products if p[0] == pid), None)
    return render_template('update.html', product=product)

# Route to delete a product
@app.route('/delete/<int:pid>')
def delete(pid):
    delete_product(pid)
    return redirect(url_for('index'))

# Route to increment stock
@app.route('/increment/<int:pid>')
def increment(pid):
    increment_stock(pid)
    return redirect(url_for('index'))

# Route to decrement stock
@app.route('/decrement/<int:pid>')
def decrement(pid):
    decrement_stock(pid)
    return redirect(url_for('index'))

#order management:
@app.route('/create_order', methods=['POST', 'GET'])
def create_order_route():
    if request.method == 'POST':
        if 'customer_id' not in request.form:
            return "Missing customer_id field", 400  # Return an error response

        customer_id = request.form['customer_id']
        status = request.form['status']
        total_amount = request.form['total_amount']

        create_order(customer_id, status, total_amount)
        return redirect(url_for('index'))

@app.route('/view_orders')
def view_purchase_orders():
    orders = get_orders()
    return render_template('orders.html', orders=orders)  # Updated to pass "orders"







# Route to generate inventory report
@app.route('/generate_report')
def generate_report_route():
    graphs = generate_report()  # Generate graphs
    if not graphs:
        graphs = {}  # Set to empty dictionary if no graphs are generated
    return render_template('report.html', graphs=graphs)

if __name__ == '__main__':
    app.run(debug=True)
