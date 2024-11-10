import gradio as gr
from qryFunctions import (
    insert_product, read_products, update_product, delete_product,
    increment_stock, decrement_stock, get_restock_notifications,
    generate_report, create_order, get_orders
)

# Function to retrieve and display products and restock notifications
def view_products():
    products = read_products()  # Get products from the database
    notifications = get_restock_notifications()  # Get restock notifications
    # Format data for DataFrames
    product_headers = ["Product ID", "Category ID", "Brand ID", "Supplier ID", "Product Name", "Stock", "Price", "Added Date"]
    notification_headers = ["Product ID", "Product Name", "Stock Level", "Restock Threshold"]
    return {"data": products, "headers": product_headers}, {"data": notifications, "headers": notification_headers}

# Functions to increment and decrement product stock
def increment_product_stock(pid):
    increment_stock(pid)  # Call the function to increment stock in the DB
    return f"Stock of product ID {pid} incremented successfully!"

def decrement_product_stock(pid):
    decrement_stock(pid)  # Call the function to decrement stock in the DB
    return f"Stock of product ID {pid} decremented successfully!"

# Function to add a product to the database
def add_product(cid, bid, sid, pname, p_stock, price, added_date):
    insert_product(cid, bid, sid, pname, p_stock, price, added_date)
    return "Product added successfully!"

# Function to generate reports (graphs)
def generate_report_gradio():
    report_graphs = generate_report()  # Call the report generation function from qryFunctions
    if report_graphs:
        stock_html = f"<img src='data:image/png;base64,{report_graphs['stock_levels']}'/>"
        sales_html = f"<img src='data:image/png;base64,{report_graphs['sales_trend']}'/>"
        status_html = f"<img src='data:image/png;base64,{report_graphs['order_status']}'/>"
        return stock_html, sales_html, status_html
    else:
        return "Error generating report", "", ""

# Define Gradio Interface
with gr.Blocks() as demo:
    gr.Markdown("# Inventory Management System")

    with gr.Tab("View Products"):
        # Display products and restock notifications
        products_output = gr.Dataframe()
        notifications_output = gr.Dataframe()
        view_btn = gr.Button("View All Products")
        view_btn.click(view_products, [], [products_output, notifications_output])

        # Stock increment and decrement controls
        pid_increment = gr.Number(label="Product ID to Increment Stock")
        increment_output = gr.Textbox(label="Increment Output")
        increment_btn = gr.Button("Increment Stock")
        increment_btn.click(increment_product_stock, [pid_increment], increment_output)

        pid_decrement = gr.Number(label="Product ID to Decrement Stock")
        decrement_output = gr.Textbox(label="Decrement Output")
        decrement_btn = gr.Button("Decrement Stock")
        decrement_btn.click(decrement_product_stock, [pid_decrement], decrement_output)

    with gr.Tab("Add Product"):
        cid = gr.Textbox(label="Category ID")
        bid = gr.Textbox(label="Brand ID")
        sid = gr.Textbox(label="Supplier ID")
        pname = gr.Textbox(label="Product Name")
        p_stock = gr.Textbox(label="Product Stock")
        price = gr.Textbox(label="Price")
        added_date = gr.Textbox(label="Added Date")
        add_output = gr.Textbox(label="Output")
        add_btn = gr.Button("Add Product")
        add_btn.click(add_product, [cid, bid, sid, pname, p_stock, price, added_date], add_output)

    with gr.Tab("Update Product"):
        pid = gr.Number(label="Product ID")
        pname = gr.Textbox(label="Product Name")
        p_stock = gr.Textbox(label="Product Stock")
        price = gr.Textbox(label="Price")
        update_output = gr.Textbox(label="Output")
        update_btn = gr.Button("Update Product")
        update_btn.click(update_product, [pid, pname, p_stock, price], update_output)

    with gr.Tab("Delete Product"):
        pid = gr.Number(label="Product ID")
        delete_output = gr.Textbox(label="Output")
        delete_btn = gr.Button("Delete Product")
        delete_btn.click(delete_product, [pid], delete_output)

    with gr.Tab("Create Order"):
        customer_id = gr.Textbox(label="Customer ID")
        status = gr.Textbox(label="Order Status")
        total_amount = gr.Number(label="Total Amount")
        order_output = gr.Textbox(label="Output")
        order_btn = gr.Button("Create Order")
        order_btn.click(create_order, [customer_id, status, total_amount], order_output)

    with gr.Tab("View Orders"):
        orders_output = gr.Dataframe()
        view_orders_btn = gr.Button("View All Orders")
        view_orders_btn.click(get_orders, [], orders_output)

    with gr.Tab("Generate Report"):
        report_stock_output = gr.HTML(label="Stock Level by Product")
        report_sales_output = gr.HTML(label="Sales Trend Over Time")
        report_status_output = gr.HTML(label="Order Status Distribution")
        report_btn = gr.Button("Generate Report")
        report_btn.click(generate_report_gradio, [], [report_stock_output, report_sales_output, report_status_output])

# Launch Gradio app
demo.launch(share=True)
