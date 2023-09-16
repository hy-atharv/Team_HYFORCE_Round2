import random
import sqlite3
import pandas as pd
import time
from pathlib import Path

Path('sales.db').touch()
# Create a list of common product IDs
com_products = range(7001, 8001)

# Create a DataFrame for sales
sales_data = []
for product_id in com_products:
    quantity = random.randint(0, 10)  # Mock quantity sold

    price = round(random.uniform(10, 4000), 2)  # Mock price
    sales_data.extend([[product_id, price, quantity]])

# Create a DataFrame for sales
sales_df = pd.DataFrame(sales_data, columns=['Product_ID', 'Price', 'Total_Quantity_Sold'])

# Save the DataFrame to a CSV file
sales_df.to_csv('mock_sales_data.csv', index=False)
conn = sqlite3.connect('sales.db')
c = conn.cursor()
# c.execute('''CREATE TABLE sales(Product_ID int, Price float, Total_Quantity_Sold int)''')
sales = pd.read_csv('mock_sales_data.csv')
sales.to_sql('sales', conn, if_exists='replace', index=False)
# Generate mock customer behavior data
behavior_data = []
for product_id in com_products:
    df = pd.read_csv('mock_sales_data.csv')
    row = df.loc[df['Product_ID'] == product_id]
    quantity_sold = row['Total_Quantity_Sold'].values[0]
    customer_ids = random.sample(range(1001, 2001), quantity_sold)  # Randomly select customer IDs for purchases
    behavior_data.extend([[customer_id, product_id, 'purchase'] for customer_id in customer_ids])
    remaining_customer_ids = [cid for cid in range(1001, 2001) if cid not in customer_ids]
    for _ in range(random.randint(0, 10)):  # Generate random click or view actions for remaining customers
        behavior_data.append([random.choice(remaining_customer_ids), product_id, random.choice(['click', 'view'])])

# Create a DataFrame for behavior
behavior_df = pd.DataFrame(behavior_data, columns=['Customer_ID', 'Product_ID', 'Action'])

# Save the DataFrame to a CSV file
behavior_df.to_csv('mock_customer_behavior_data.csv', index=False)

# Load the customer behavior data from the CSV file
behavior_df = pd.read_csv('mock_customer_behavior_data.csv')
# c.execute('''CREATE TABLE customer_behavior(Customer_ID int, Product_ID int, Action str)''')
customer_behavior = pd.read_csv('mock_customer_behavior_data.csv')
customer_behavior.to_sql('customer_behavior', conn, if_exists='replace', index=False)
# Filter the DataFrame to select only "purchase" actions
purchase_df = behavior_df[behavior_df['Action'] == 'purchase']

reviews_list = ["I absolutely love this product! It's a game-changer.",
                "Not what I expected. Disappointed with the quality.",
                "Incredible value for the price. Highly recommended.", "Meh, it's just okay. Not great, not terrible.",
                "Worst purchase ever. Regret buying this.", "Impressed by the fast delivery. Great service.",
                "The product exceeded my expectations. Very happy!", "Wouldn't buy it again. It broke within a week.",
                "A must-have for anyone! Can't imagine life without it.",
                "It's decent, but there are better options out there.",
                "Arrived damaged, but customer support was helpful.",
                "I can't stop raving about this product. It's amazing!", "Not worth the money. Very poor quality.",
                "Five stars all the way! I'm a satisfied customer.", "Product as described. No complaints here.",
                "I expected more. It's just meh.", "Huge improvement in my daily routine. Thank you!",
                "It broke on the first use. Total waste of money.", "Perfect! Exactly what I was looking for.",
                "It's okay, but it didn't meet my expectations.", "Prompt delivery and the product is top-notch.",
                "Terrible! Don't waste your money.", "I'm in love with this product. So worth it!",
                "Not bad, but there's room for improvement.", "Outstanding value for the price. Highly recommended.",
                "It didn't meet my expectations. Just average.", "Fast shipping and a great product. Happy customer!",
                "I wish I hadn't bought this. It's useless.", "Good value for the price. I'm content.",
                "This product is a game-changer. I'm thrilled!", "It's not worth the price. Very overrated.",
                "I'm blown away by how amazing this is!", "It's decent, but there are better options.",
                "Life-changing product. I can't thank you enough.", "I regret buying this. It's a letdown.",
                "Exactly what I needed. Very satisfied.", "This product is a game-changer. I'm thrilled!",
                "It's not terrible, but it's not great either.", "Arrived on time, but the product is subpar.",
                "I'm in love with this product. So worth it!", "Not bad, but there's room for improvement.",
                "Exceptional quality. I'm impressed!", "I expected better. It's just average.",
                "Life-changing product. I can't thank you enough.", "I regret buying this. It's a letdown.",
                "I'm blown away by how amazing this is!", "Not worth the money. Poor quality.",
                "I can't believe I waited this long to buy it. Love it!",
                "It's decent for the price, but don't expect miracles.", "Excellent product and service. A+.",
                "It broke within days. Very disappointed.", "Impressive quality. I'm a satisfied customer.",
                "Meh, it's okay. Nothing special.", "This product is a lifesaver. So grateful!",
                "Outstanding value for money. Highly recommended.", "It didn't meet my expectations. Just average.",
                "Fast shipping and a great product. Very happy!", "I'm in love with this product. Can't get enough.",
                "It's not terrible, but it's not outstanding either.",
                "Top-notch customer service. The product, not so much.", "Exactly what I needed. Very satisfied.",
                "This product is a game-changer. I'm thrilled!", "It's not worth the price. Very overrated.",
                "I'm blown away by how amazing this is!", "It's decent, but there are better options.",
                "Life-changing product. I can't thank you enough.", "I regret buying this. It's a letdown.",
                "Good value for the money. I'm content.", "The quality is outstanding. Highly recommended.",
                "Not impressed. It didn't live up to the hype.", "Fast shipping and a great product. Happy customer!",
                "I wish I hadn't bought this. It's useless.", "Customer service was excellent. Product, not so much.",
                "My new favorite! Can't get enough of it.", "I got what I paid for. It's decent.",
                "Perfect! Exactly what I was looking for.", "It's okay, but it didn't meet my expectations.",
                "Prompt delivery and the product is top-notch.", "Terrible! Don't waste your money.",
                "I'm in love with this product. So worth it!", "Not bad, but there's room for improvement.",
                "Exceptional quality. I'm impressed!", "I expected better. It's just average.",
                "Life-changing product. I can't thank you enough.", "I regret buying this. It's a letdown.",
                "I'm blown away by how amazing this is!", "Not worth the money. Poor quality.",
                "I can't believe I waited this long to buy it. Love it!",
                "It's decent for the price, but don't expect miracles.", "Excellent product and service. A+.",
                "It broke within days. Very disappointed.", "Impressive quality. I'm a satisfied customer.",
                "Meh, it's okay. Nothing special.", "This product is a lifesaver. So grateful!",
                "Outstanding value for money. Highly recommended.", "It didn't meet my expectations. Just average.",
                "Fast shipping and a great product. Very happy!", "I'm in love with this product. Can't get enough.",
                "It's not terrible, but it's not outstanding either.", "This product is a game-changer. I'm thrilled!",
                "Absolutely terrible. Wouldn't recommend.", "Impressed with the quality. Worth every penny.",
                "Average product. Nothing to write home about.", "Fast shipping and great service.",
                "Not as described. Disappointed with the purchase.", "Five-star experience all around!",
                "It's just okay. Expected better.", "Best purchase I've made in a while!",
                "Poor quality. Broke within days.", "Incredible value for the price. Highly satisfied.",
                "Mediocre at best. Expected more.", "Life-changing! Can't believe I waited so long.",
                "Regret buying this. Waste of money.", "Prompt delivery and top-notch product.",
                "Good value for the price. Content with my purchase.",
                "The product exceeded my expectations. Very happy!", "Not bad, but there are better options out there.",
                "Outstanding value for money. Highly recommended.", "Worst experience ever. Stay away.",
                "Perfect! Exactly what I needed.", "It's decent, but it didn't meet my expectations.",
                "Terrible! Don't waste your hard-earned money.", "I'm in love with this product. Can't get enough!",
                "Could be better. Not impressed.", "Exceptional quality. I'm impressed!",
                "I expected better. It's just average.", "Life-changing! Highly recommend to everyone.",
                "I regret buying this. Total letdown.", "Exactly what I needed. Very satisfied.",
                "This product is a game-changer. Thrilled with it!", "Not worth the price. Very overrated.",
                "I'm blown away by how amazing this is!", "Just okay. Won't rave about it.",
                "Fast shipping and great product. Delighted!", "Wish I hadn't bought this. It's useless.",
                "Customer service was excellent. Product, not so much.", "My new favorite! Can't live without it.",
                "Got what I paid for. It's decent.", "Great product, fast delivery. Highly recommended.",
                "It's alright, but nothing special.", "Arrived damaged, but they resolved it well.",
                "Life-saver! So grateful for this product.", "Great value for the money. Happy with my purchase.",
                "Didn't meet my expectations. Slightly disappointed.",
                "Fast shipping and a fantastic product. Very satisfied!",
                "Can't get enough of this product. Absolutely love it!", "Not terrible, but not outstanding either.",
                "Top-notch customer service. Impressed with their support.",
                "Exactly what I needed. Very content with the purchase.",
                "This product is a game-changer. Thrilled to have it!", "Not worth the money. Poor quality product.",
                "Can't believe I waited so long to buy it. It's amazing!",
                "Decent for the price, but don't expect miracles.", "Excellent product and service. A+.",
                "Broke within days. Very disappointing.", "Impressive quality. A satisfied customer here.",
                "Average at best. Nothing special.", "This product is a lifesaver. So thankful for it!",
                "Amazing value for money. Highly recommended.", "Didn't meet my expectations. Just an average product.",
                "Lightning-fast shipping and a superb product. Ecstatic!",
                "I'm in love with this product. It's a must-have!", "Not bad, but definitely room for improvement.",
                "Outstanding quality. I'm thoroughly impressed.", "Expected better. It's just okay.",
                "Truly life-changing! Can't thank you enough.", "Regret buying this. It's a disappointment.",
                "Good value for the money. I'm satisfied.", "Exceeded my expectations. Highly recommend it!",
                "It's decent, but there are better options available.", "Worst purchase ever. Avoid at all costs.",
                "Perfect! Exactly what I wanted.", "Okay, but didn't quite meet my expectations.",
                "Prompt delivery and a top-notch product.", "Terrible experience. Do not recommend.",
                "I'm head over heels for this product. It's fantastic!", "Could be better. Not overly impressed.",
                "Exceptional quality. They've won me over.", "Expected more. It's just average.",
                "Absolutely life-changing! Can't thank you enough.", "I regret buying this. It's a disappointment.",
                "Great value for the money. I'm content.", "Impressed with the quality. Highly satisfied.",
                "Not bad, but there are better options out there.", "Outstanding value for money. Highly recommended.",
                "Stay away! Terrible experience.", "Exactly what I needed. Couldn't be happier.",
                "It's decent, but it didn't fully meet my expectations.", "Fast shipping and great service. Delighted!",
                "Wish I hadn't bought this. It's not useful.", "Excellent customer service. The product, not so much.",
                "My new favorite! I can't get enough.", "Got what I paid for. It's decent.",
                "Perfect product, fast delivery. Highly recommended.", "It's alright, but nothing to write home about.",
                "Arrived damaged, but they handled it well.", "This product is a lifesaver. So thankful.",
                "Great value for the price. Happy with my purchase.",
                "Didn't fully meet my expectations. Slightly disappointed.",
                "Fast shipping and an excellent product. Very satisfied!",
                "I'm obsessed with this product. I absolutely adore it!", "Not terrible, but not exceptional either.",
                "Top-notch customer service. Impressed with their support.",
                "Exactly what I needed. Very satisfied with my purchase.",
                "This product is a game-changer. Thrilled to have it!", "Not worth the money. Poor quality.",
                "Can't believe I waited this long to buy it. It's amazing!",
                "Decent for the price, but don't expect miracles.", "Excellent product and excellent service. A+.",
                "Broke within days. Very disappointing.", "Impressive quality. A satisfied customer here.",
                "Average at best. Nothing special.", "This product is a lifesaver. So thankful for it!",
                "Fantastic value for money. Highly recommended.",
                "Didn't fully meet my expectations. Just an average product.",
                "Blazing-fast shipping and an outstanding product. Ecstatic!",
                "I'm in love with this product. It's a must-have!",
                "Not bad, but definitely some room for improvement.", "Outstanding quality. I'm thoroughly impressed.",
                "Expected better. It's just okay.", "Absolutely life-changing! Can't thank you enough.",
                "I regret buying this. It's a disappointment.", "Good value for the money. I'm satisfied.",
                "Exceeded my expectations. Highly recommend it!",
                "It's decent, but there are better options available.", "Worst purchase ever. Avoid at all costs.",
                "Perfect! Exactly what I wanted.", "Okay, but didn't quite meet my expectations.",
                "Prompt delivery and a top-notch product.", "Terrible experience. Do not recommend.",
                "I'm head over heels for this product. It's fantastic!", "Could be better. Not overly impressed.",
                "Exceptional quality. They've won me over.", "Expected more. It's just average.",
                "Absolutely life-changing! Can't thank you enough.", "I regret buying this. It's a disappointment.",
                "Great value for the money. I'm content.", "Impressed with the quality. Highly satisfied.",
                "Not bad, but there are better options out there.", "Outstanding value for money. Highly recommended.",
                "Stay away! Terrible experience.", "Exactly what I needed. Couldn't be happier.",
                "It's decent, but it didn't fully meet my expectations.", "Fast shipping and great service. Delighted!",
                "Wish I hadn't bought this. It's not useful.", "Excellent customer service. The product, not so much.",
                "My new favorite! I can't get enough.", "Got what I paid for. It's decent.",
                "Perfect product, fast delivery. Highly recommended.", "It's alright, but nothing to write home about.",
                "Arrived damaged, but they handled it well.", "This product is a lifesaver. So thankful.",
                "Great value for the price. Happy with my purchase.",
                "Didn't fully meet my expectations. Slightly disappointed.",
                "Fast shipping and an excellent product. Very satisfied!",
                "I'm obsessed with this product. I absolutely adore it!", "Not terrible, but not exceptional either.",
                "Top-notch customer service. Impressed with their support.",
                "Exactly what I needed. Very satisfied with my purchase."

                ]
# Create a list to store Product_id, Customer_id, and Review
selected_reviews = []

# Iterate through the purchase_df and randomly select reviews
for index, row in purchase_df.iterrows():
    product_id = row['Product_ID']
    customer_id = row['Customer_ID']
    # Randomly select a review from the reviews_list
    random_review = random.choice(reviews_list)
    review_score = 0  # random.randint(2, 10)
    selected_reviews.append([product_id, customer_id, random_review, review_score])

# Create a new DataFrame for Product_id, Customer_id, and Review
final_df = pd.DataFrame(selected_reviews, columns=['Product_ID', 'Customer_ID', 'Review', 'Review_Score'])
final_df.to_csv('mock_customer_info_&_review.csv', index=False)

# c.execute('''CREATE TABLE customer_reviews(Product_ID int, Customer_ID int, Review str)''')
customer_reviews = pd.read_csv('mock_customer_info_&_review.csv')
customer_reviews.to_sql('customer_reviews', conn, if_exists='replace', index=False)
# Generate mock competitor pricing data
competitor_pricing_data = []

for product_id in com_products:
    df = pd.read_csv('mock_sales_data.csv')
    price = df.loc[df['Product_ID'] == product_id, 'Price'].values[0]

    competitor_price = price * (1 + random.uniform(-0.10, 0.20))
    competitor_price = round(competitor_price, 2)
    competitor_pricing_data.append([product_id, competitor_price])

# Create a DataFrame
competitor_df = pd.DataFrame(competitor_pricing_data, columns=['Product_ID', 'Competitor_Price'])

# Save the DataFrame to a CSV file
competitor_df.to_csv('mock_competitor_pricing_data.csv', index=False)

df2 = pd.read_csv("mock_competitor_pricing_data.csv")


#This Loop is changing the competitor prices for the products after every 5 to 10 secs
while True:
    time.sleep(random.uniform(5, 10))
    for product_id in com_products:
        comp_price = competitor_df.loc[competitor_df['Product_ID'] == product_id, 'Competitor_Price'].values[0]
        dynamic_price = comp_price * (1 + random.uniform(-0.10, 0.20))
        dynamic_price = round(dynamic_price, 2)
        # Update the DataFrame with the new dynamic price
        df2.loc[df2['Product_ID'] == product_id, 'Competitor_Price'] = dynamic_price

        # Save the updated DataFrame to the CSV file
    df2.to_csv('mock_competitor_pricing_data.csv', index=False)
    # c.execute('''CREATE TABLE competitor_price(Product_ID int, Competitor_Price float)''')
    competitor_price = pd.read_csv('mock_competitor_pricing_data.csv')
    competitor_price.to_sql('competitor_price', conn, if_exists='replace', index=False)
