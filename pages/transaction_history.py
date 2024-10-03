import streamlit as st
import mysql.connector
import os
from dotenv import load_dotenv
import pandas as pd

# Load environment variables from .env file
load_dotenv()

# Database connection
def connect_to_db():
    conn = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )
    return conn

# Function to fetch transactions for a specific user
def fetch_transactions(user_id):
    conn = connect_to_db()
    cursor = conn.cursor(dictionary=True)
    
    query = "SELECT * FROM Transactions WHERE user_id = %s ORDER BY transaction_date DESC"
    cursor.execute(query, (user_id,))
    transactions = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return transactions

# Page layout for Transaction History
def transaction_history_page():
    st.title("Transaction History")
    
    # Input for User ID to fetch specific user's transactions
    user_id = st.text_input("Enter User ID:")
    
    if user_id:
        transactions = fetch_transactions(user_id)
        
        if transactions:
            df = pd.DataFrame(transactions)
            st.write("Your Transactions:")
            st.dataframe(df)
        else:
            st.write("No transactions found for this User ID.")

# Run the page function
if __name__ == "__main__":
    transaction_history_page()
