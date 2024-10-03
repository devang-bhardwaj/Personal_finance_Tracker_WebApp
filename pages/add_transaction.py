import streamlit as st
import mysql.connector
import os
from dotenv import load_dotenv

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

# Page layout for Add Transactions
def add_transaction_page():
    st.title("Add Transaction")

    # Form for inputting transaction data
    with st.form("transaction_form"):
        user_id = st.text_input("User ID")  # Assuming user_id is required for each user
        transaction_type = st.selectbox("Transaction Type", ["Income", "Expense", "Transferred"])
        amount = st.number_input("Amount", min_value=0.01)
        description = st.text_input("Description")
        date = st.date_input("Transaction Date")
        
        submit_button = st.form_submit_button(label="Add Transaction")

    # Inserting data into the database
    if submit_button:
        conn = connect_to_db()
        cursor = conn.cursor()

        # SQL query to insert data
        query = """
        INSERT INTO Transactions (user_id, transaction_type, amount, description, transaction_date)
        VALUES (%s, %s, %s, %s, %s)
        """
        values = (user_id, transaction_type, amount, description, date)

        try:
            cursor.execute(query, values)
            conn.commit()
            st.success("Transaction added successfully!")
        except mysql.connector.Error as err:
            st.error(f"Error: {err}")
        finally:
            cursor.close()
            conn.close()

# Run the page function
if __name__ == "__main__":
    add_transaction_page()
