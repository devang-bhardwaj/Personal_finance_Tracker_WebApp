import streamlit as st
import os
from dotenv import load_dotenv
import mysql.connector

# Load environment variables from .env file
load_dotenv()

def connect_to_db():
    conn = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )
    return conn

def fetch_budgets(user_id):
    conn = connect_to_db()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM Budget WHERE user_id = %s"
    cursor.execute(query, (user_id,))
    budgets = cursor.fetchall()
    cursor.close()
    conn.close()
    return budgets

def add_budget(user_id, description, amount, category):
    conn = connect_to_db()
    cursor = conn.cursor()
    query = "INSERT INTO Budget (user_id, description, amount, category) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (user_id, description, amount, category))
    conn.commit()
    cursor.close()
    conn.close()

# Budget Page
st.title("Budget Management")

user_id = st.session_state.user_id  # Get user ID from session state

# Input for new budget item
st.header("Add New Budget Item")
description = st.text_input("Description")
amount = st.number_input("Amount", min_value=0.0, format="%.2f")
category = st.text_input("Category (Optional)")

if st.button("Add Budget Item"):
    if description and amount > 0:
        add_budget(user_id, description, amount, category)
        st.success("Budget item added successfully!")
    else:
        st.error("Please enter valid values.")

# Display Existing Budgets
st.header("Current Budgets")
budgets = fetch_budgets(user_id)

if budgets:
    for budget in budgets:
        st.write(f"{budget['description']} - ₹{budget['amount']} - {budget['category']}")
else:
    st.write("No budgets found.")

# Calculate total budgeted amount
total_budget = sum(budget['amount'] for budget in budgets) if budgets else 0.0
st.write(f"Total Budgeted Amount: ₹{total_budget:.2f}")
