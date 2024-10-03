import streamlit as st
import mysql.connector

def run():
    st.title("Account Balance")

    # Connect to the database
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='DVNG@dvng@181204',  # your password
        database='personal_finance_tracker'  # your database name
    )
    
    cursor = conn.cursor()

    # Calculate balance
    query_income = "SELECT SUM(amount) FROM transactions WHERE user_id = %s AND transaction_type = 'Income'"
    cursor.execute(query_income, (1,))  # Replace 1 with the current user's ID
    total_income = cursor.fetchone()[0] or 0

    query_expense = "SELECT SUM(amount) FROM transactions WHERE user_id = %s AND transaction_type = 'Expense'"
    cursor.execute(query_expense, (1,))  # Replace 1 with the current user's ID
    total_expense = cursor.fetchone()[0] or 0

    balance = total_income - total_expense

    st.write(f"Total Income: {total_income}")
    st.write(f"Total Expense: {total_expense}")
    st.write(f"Current Balance: {balance}")

    cursor.close()
    conn.close()
