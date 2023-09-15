import os
import pandas as pd
import openai
import sqlite3
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

conn = sqlite3.connect('sales.db')
cursor = conn.cursor()

# Query to retrieve customer_id and number of clicks
clicks_query = """
    SELECT Customer_ID, COUNT(*) AS number_of_clicks
    FROM customer_behavior
    WHERE Action = 'click'
    GROUP BY Customer_ID
"""

# Query to retrieve customer_id and number of views
views_query = """
    SELECT Customer_ID, COUNT(*) AS number_of_views
    FROM customer_behavior
    WHERE Action = 'view'
    GROUP BY Customer_ID
"""

# Query to retrieve customer_id and mean review score
review_query = """
    SELECT Customer_ID, ROUND(AVG(Review_Score), 2) AS mean_review_score
    FROM customer_reviews
    GROUP BY Customer_ID
"""

# Execute the queries and fetch data into DataFrames
clicks_data = pd.read_sql_query(clicks_query, conn)
views_data = pd.read_sql_query(views_query, conn)
review_data = pd.read_sql_query(review_query, conn)

# Merge the DataFrames on 'Customer_ID'
customer_data = clicks_data.merge(views_data, on='Customer_ID', how='outer')
customer_data = customer_data.merge(review_data, on='Customer_ID', how='outer')
customer_data = customer_data.fillna(0)
customer_data.to_csv('customer_data.csv', index=False)
customer_data.to_sql('customer_data', conn, if_exists='replace', index=False)
# Use the ALTER TABLE statement to add columns
cursor.execute('ALTER TABLE customer_data ADD COLUMN discount REAL')
cursor.execute('ALTER TABLE customer_data ADD COLUMN engaging REAL')

# Create dictionaries to store the data
customer_ids = {}
number_of_clicks = {}
number_of_views = {}
mean_review_scores = {}

# Fetch data from the customer_data table where discount is NULL
cursor.execute(
    "SELECT Customer_ID, number_of_clicks, number_of_views, mean_review_score FROM customer_data WHERE discount IS NULL")

# Fetch all the rows
rows = cursor.fetchmany(3)

# Iterate through the rows and populate the dictionaries
for row in rows:
    customer_id, clicks, views, review_score = row
    customer_ids[customer_id] = customer_id
    number_of_clicks[customer_id] = clicks
    number_of_views[customer_id] = views
    mean_review_scores[customer_id] = review_score

for c in customer_ids:
    clicks_num = number_of_clicks[c]
    views_num = number_of_views[c]
    rev_score = mean_review_scores[c]
    customer = customer_ids[c]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a customer behavior analyst and your job is to analyse the customer "
                           "engagement:\nnumber of clicks by customer\nnumber of views by customer\nmean review score "
                           "customer gave\nOn the basis of this data, you have to decide the discount % for the "
                           "customer from 0 to 4%. In your answer, write ONLY number without percentage symbol or any word"
            },
            {
                "role": "user",
                "content": "number of clicks:" + str(clicks_num) + "\n" + "number of views:" + str(
                    views_num) + "\n" + "mean review score:" + str(rev_score)


            }
        ],
        temperature=0.8,
        max_tokens=1,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    discount = response['choices'][0]['message']['content']

    # Update the database with the discount for a customer
    cursor.execute("UPDATE customer_data SET discount = ? WHERE Customer_ID = ?",
                   (discount, customer))

    # Commit the changes to the database
    conn.commit()

# Close the database connection
conn.close()
