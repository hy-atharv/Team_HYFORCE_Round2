import pandas as pd
import sqlite3
import numpy as np

''' 
> For Training the Model in future using Gradient Boost ML Algorithm <
import xgboost as xgb  
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from scipy.optimize import linprog
'''

# database connection and retrieval function
conn = sqlite3.connect('sales.db')


def retrieve_pricing_data():
    query = """
        SELECT s.Product_ID, s.Price, c.Competitor_Price, s.Total_Quantity_Sold,
               r.Mean_Review_Score
        FROM sales s
        LEFT JOIN competitor_price c ON s.Product_ID = c.Product_ID
        LEFT JOIN (
            SELECT Product_ID, ROUND( AVG(Review_Score),2 ) as Mean_Review_Score
            FROM customer_reviews
            GROUP BY Product_ID
        ) r ON s.Product_ID = r.Product_ID
        """
    df = pd.read_sql_query(query, conn)

    # Calculate Number_of_Clicks and Number_of_Views for each product
    # Iterate through customer_behavior table
    click_counts = []
    view_counts = []
    for product_id in df['Product_ID']:
        click_query = f"SELECT COUNT(*) FROM customer_behavior WHERE Product_ID = '{product_id}' AND Action = 'click'"
        view_query = f"SELECT COUNT(*) FROM customer_behavior WHERE Product_ID = '{product_id}' AND Action = 'view'"
        click_count = conn.execute(click_query).fetchone()[0]
        view_count = conn.execute(view_query).fetchone()[0]
        click_counts.append(click_count)
        view_counts.append(view_count)

    df['Number_of_Clicks'] = click_counts
    df['Number_of_Views'] = view_counts

    return df


a = retrieve_pricing_data()
a.to_csv('dataset.csv', index=False)
dataset = pd.read_csv('dataset.csv')
dataset.to_sql('dataset', conn, if_exists='replace', index=False)


def execute_query1(query, values):
    try:
        cursor = conn.cursor()
        cursor.execute(query, values)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error executing query: {e}")


def execute_query2(query):
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        return result[0] if result else None
    except sqlite3.Error as e:
        print(f"Error executing query: {e}")


def execute_query3(query):
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error executing query: {e}")


def optimal_pricing():
    price_data = retrieve_pricing_data()
    # Calculate the total sales by summing the products of Price and Total_Quantity_Sold
    prev_sales = (price_data['Price'] * price_data['Total_Quantity_Sold']).sum()
    # Declare weightage values for different factors
    weight_quantity_sold = 0.4
    weight_price_difference = 0.2
    weight_mean_review_score = 0.2
    weight_number_of_clicks = 0.15
    weight_number_of_views = 0.05

    # Iterate through the DataFrame for each product_id
    for _, row in price_data.iterrows():
        product_id = row['Product_ID']
        price = row['Price']
        competitor_price = row['Competitor_Price']
        total_quantity_sold = row['Total_Quantity_Sold']
        mean_review_score = row['Mean_Review_Score']
        number_of_clicks = row['Number_of_Clicks']
        number_of_views = row['Number_of_Views']

        # Calculate percentage price difference
        percentage_price_difference = ((competitor_price - price) * 100) / price

        # Calculate final weight

        if total_quantity_sold == 0:
            final_weight = ((weight_price_difference * percentage_price_difference) +
                            (weight_number_of_clicks * number_of_clicks) +
                            (weight_number_of_views * number_of_views))

        else:
            final_weight = ((weight_quantity_sold * total_quantity_sold) +
                            (weight_price_difference * percentage_price_difference) +
                            (weight_mean_review_score * mean_review_score) +
                            (weight_number_of_clicks * number_of_clicks) +
                            (weight_number_of_views * number_of_views))

        # Calculate optimal price
        optimal_price = round((price + (final_weight * price) / 100), 2)

        query1 = """
        UPDATE sales
        SET Price = ?
        WHERE Product_ID = ?
        """

        values = (optimal_price, product_id)

        # Execute the query to update the sales table
        execute_query1(query1, values)

    query2 = """
        SELECT SUM(Price * Total_Quantity_Sold)
        FROM sales
        """

    new_sales = execute_query2(query2)

    revenue = "Sales Before optimal prices:\n$" + str(
        round(prev_sales, 3)) + "\nSales After optimal prices if same customer responses:\n$" + str(
        round(new_sales, 3)) + "\nSales increased by " + str(
        round(((new_sales - prev_sales) * 100) / prev_sales, 4)) + "%"

    # Setting Quantity data to 0 to store new values of quantity for new optimal prices
    update_query = "UPDATE sales SET Total_Quantity_Sold = 0"
    execute_query3(update_query)

    print(revenue)


optimal_pricing()
