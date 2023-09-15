from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import pandas as pd
import webbrowser

app = Flask(__name__)


@app.route('/', methods=['GET'])
def login():
    if request.method == 'POST':
        customer_id = request.form.get('customer_id')
        # Perform any necessary validation on the customer_id here
        # Once validated, redirect to the product display page
        return redirect(url_for('products', customer_id=customer_id))
    return render_template('login.html')


@app.route('/products', methods=['GET'])
def products():
    # Retrieve the customer_id from the query parameters
    customer_id = request.args.get('customer_id')

    # Create a new database connection within this route function
    conn = sqlite3.connect('sales.db')

    # Retrieve Product_ID and Action for the given customer_id
    query = f"SELECT Product_ID, Action FROM customer_behavior WHERE Customer_ID = {customer_id}"
    behavior_data = pd.read_sql_query(query, conn)

    # Identify all unique Product_IDs in the sales table
    all_products_query = "SELECT DISTINCT Product_ID FROM sales"
    all_product_ids = pd.read_sql_query(all_products_query, conn)['Product_ID'].tolist()

    # Create a DataFrame with all unique Product_IDs
    all_products_data = pd.DataFrame({'Product_ID': all_product_ids})

    # Retrieve Price values from the sales table for all products
    query = "SELECT Product_ID, Price FROM sales"
    price_data = pd.read_sql_query(query, conn)

    # Merge behavior_data and all_products_data to ensure all products are included
    merged_data = pd.merge(all_products_data, behavior_data, on='Product_ID', how='left')

    # Merge price_data with merged_data to add Price information
    merged_data = pd.merge(merged_data, price_data, on='Product_ID', how='left')

    # Define the sorting order based on Action
    sorting_order = ['purchase', 'view', 'click']

    # Sort the merged data based on the specified order
    merged_data['Action'] = pd.Categorical(merged_data['Action'], categories=sorting_order, ordered=True)
    merged_data = merged_data.sort_values(by=['Action'], ascending=False)

    conn.close()
    # Pass the sorted merged data to the HTML template
    return render_template('products.html', products=merged_data.values, customer_id=customer_id)


@app.route('/offers/<customer_id>', methods=['GET'])
def offers(customer_id):
    conn = sqlite3.connect('sales.db')
    cursor = conn.cursor()
    cursor.execute("SELECT discount FROM customer_data WHERE Customer_ID = ?", (customer_id,))
    result1 = cursor.fetchone()
    discount = result1[0]
    cursor.execute(
        "SELECT DISTINCT Product_ID FROM customer_behavior WHERE Customer_ID = ? AND (Action = 'view' OR Action = 'click')",
        (customer_id,))
    result2 = cursor.fetchall()
    products = [row[0] for row in result2]
    cursor.close()

    # Debugging print statement
    print("Products:", products)

    return render_template('offers.html', discount=discount, products=products)


host = '127.0.0.1'
port = 3000

# Open the default web browser to the Flask app's URL
url = f'http://{host}:{port}'
webbrowser.open(url)

# Start the Flask app
app.run(host=host, port=port)