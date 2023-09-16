import os
import openai
import random
import sqlite3
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

conn = sqlite3.connect('sales.db')
cursor = conn.cursor()
# Query the database to get a list of reviews with a score of 0
cursor.execute("SELECT Review, Review_Score FROM customer_reviews WHERE Review_Score==0")

# Fetch a batch of reviews
# In my case since I dont have a paid account for the OpenAI API
# I can send only  3 requests per minute
# But just for $0.002 per 1K Tokens, an organisation can send 3500 requests and 90000 tokens per minute with a paid acount
batch_size = 3  
reviews_to_score = cursor.fetchmany(batch_size)

for rev in reviews_to_score:
    review = rev[0]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a customer reviews analyst and your job is to analyse the given review, "
                           "rate it on a scale from 1 to 10 and reply with just the number"
            },
            {
                "role": "user",
                "content": review
            }
        ],
        temperature=0.8,
        max_tokens=1,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    score = response['choices'][0]['message']['content']

    # Update the database with the review score
    cursor.execute("UPDATE customer_reviews SET Review_Score = ? WHERE Review = ?",
                   (score, review))

conn.commit()
# Close the database connection
conn.close()
