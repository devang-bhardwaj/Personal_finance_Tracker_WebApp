import streamlit as st
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def connect_to_db():
    conn = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )
    return conn

# Function to fetch user transactions from the database
def fetch_user_transactions(user_id):
    conn = connect_to_db()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM transactions WHERE user_id = %s"
    cursor.execute(query, (user_id,))
    transactions = cursor.fetchall()
    conn.close()
    return transactions

# Function to calculate income, expenses, and balance
def calculate_summary(transactions):
    income = sum(txn['amount'] for txn in transactions if txn['transaction_type'] == 'Income')
    expenses = sum(txn['amount'] for txn in transactions if txn['transaction_type'] == 'Expense')
    balance = income - expenses
    return income, expenses, balance

# Function to plot graphs
def plot_income_vs_expenses(income, expenses):
    labels = ['Income', 'Expenses']
    values = [income, expenses]

    fig, ax = plt.subplots()
    ax.bar(labels, values, color=['green', 'red'])
    ax.set_title('Income vs Expenses')
    st.pyplot(fig)

# Function to create pie chart for expense breakdown
def plot_expense_breakdown(transactions):
    categories = [txn['description'] for txn in transactions if txn['transaction_type'] == 'Expense']
    amounts = [txn['amount'] for txn in transactions if txn['transaction_type'] == 'Expense']

    fig, ax = plt.subplots()
    ax.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)

# Main Application
st.title("Financial Statistics")

# Input User ID
user_id = st.text_input("Enter User ID:", "")

if user_id:
    # Fetch user transactions
    transactions = fetch_user_transactions(user_id)

    if transactions:
        # Calculate summary
        total_income, total_expenses, balance = calculate_summary(transactions)

        # Display Summary
        st.header("Summary")
        st.write(f"Total Income: ₹{total_income}")
        st.write(f"Total Expense: ₹{total_expenses}")
        st.write(f"Balance: ₹{balance}")

        # Plot Income vs Expenses
        st.header("Income vs Expenses")
        plot_income_vs_expenses(total_income, total_expenses)

        # Plot Expense Breakdown
        st.header("Expense Breakdown")
        plot_expense_breakdown(transactions)

        # Show Transaction History (Optional)
        st.header("Transaction History")
        df = pd.DataFrame(transactions)
        st.write(df)

    else:
        st.write("No transactions found for this user.")
else:
    st.write("Please enter a User ID to view financial statistics.")
