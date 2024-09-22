import streamlit as st
import mysql.connector
import bcrypt
from streamlit_option_menu import option_menu
import os

# Dummy user data (Replace with MySQL query for real implementation)
users = {'user1': {'password': bcrypt.hashpw('password123'.encode('utf-8'), bcrypt.gensalt())}}

# Check if user is logged in using session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Login Form
def login_form():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        # Fetch user data from database
        user_data = users.get(username)
        if user_data and bcrypt.checkpw(password.encode('utf-8'), user_data['password']):
            st.session_state.logged_in = True
            st.success("Logged in successfully!")
            st.experimental_rerun()
        else:
            st.error("Invalid username or password")

# Sign Up Form
def signup_form():
    st.title("Sign Up")
    username = st.text_input("Choose a username")
    password = st.text_input("Choose a password", type="password")
    if st.button("Sign Up"):
        if username in users:
            st.error("Username already exists")
        else:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            users[username] = {'password': hashed_password}
            st.success("Account created successfully! Please log in.")
            st.experimental_rerun()

# Logout Function
def logout():
    st.session_state.logged_in = False
    st.experimental_rerun()

# Main Dashboard Page (shown after login)
def main_dashboard():
    st.title("Personal Finance Tracker Dashboard")

    # Dropdown menu with logout option
    selected = option_menu(
        menu_title=None,
        options=["Dashboard", "Add Transaction", "Transaction History", "Accounts"],
        icons=["house", "plus", "list", "wallet"],
        menu_icon="cast",
        default_index=0,
    )
    
    if selected == "Dashboard":
        st.subheader("Overview of your Financial Data")
    elif selected == "Add Transaction":
        add_transaction_form()
    elif selected == "Transaction History":
        display_transaction_history()
    elif selected == "Accounts":
        st.subheader("Your Account Balances")
    
    # Dropdown menu logout option
    with st.sidebar:
        if st.button("Log Out"):
            logout()

# Add Transaction Form
def add_transaction_form():
    st.title("Add a New Transaction")
    transaction_type = st.selectbox("Transaction Type", ["Income", "Expense", "Transfer"])
    amount = st.number_input("Amount", min_value=0.01, step=0.01)
    category = st.text_input("Category")
    date = st.date_input("Date")
    account = st.text_input("Account")
    
    if st.button("Add Transaction"):
        # Insert transaction into the database
        st.success(f"Transaction of {amount} added successfully!")

# Transaction History Page
def display_transaction_history():
    st.title("Transaction History")
    # Fetch from the MySQL database (dummy data for now)
    transactions = [
        {"Date": "2024-01-01", "Type": "Income", "Amount": 500, "Category": "Salary", "Account": "Bank"},
        {"Date": "2024-01-05", "Type": "Expense", "Amount": -100, "Category": "Groceries", "Account": "Bank"},
    ]
    st.table(transactions)

# Handle login and redirect to dashboard after login
if st.session_state.logged_in:
    main_dashboard()
else:
    login_signup_tab = st.sidebar.radio("Login/Sign Up", ("Login", "Sign Up"))
    if login_signup_tab == "Login":
        login_form()
    elif login_signup_tab == "Sign Up":
        signup_form()
