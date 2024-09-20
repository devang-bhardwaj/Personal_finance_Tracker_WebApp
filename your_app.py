import streamlit as st
import mysql.connector
import bcrypt
import os
from dotenv import load_dotenv

load_dotenv()  # Load the .env file

def create_connection():
    connection = mysql.connector.connect(
        host="localhost",  # Update with your MySQL host
        user="root",       # Update with your MySQL user
        password=os.getenv("MYSQL_PASSWORD"),  # Get password from environment variable
        database="finance_tracker"
    )
    return connection


# Hash password
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# Verify hashed password
def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

# Sign-Up function
def sign_up():
    
    st.subheader("Create New Account")
    
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if password == confirm_password:
        if st.button("Sign Up"):
            hashed_password = hash_password(password)
            
            connection = create_connection()
            cursor = connection.cursor()

            try:
                cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, hashed_password))
                connection.commit()
                st.success("Account created successfully!")
            except mysql.connector.Error as err:
                st.error(f"Error: {err}")
            finally:
                cursor.close()
                connection.close()
    else:
        st.warning("Passwords do not match")

# Login function
def login():
    st.subheader("Login to Your Account")
    
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        connection = create_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT password FROM users WHERE email=%s", (email,))
        result = cursor.fetchone()

        if result:
            hashed_password = result[0].encode('utf-8')  # Convert hashed password to bytes
            
            if check_password(password, hashed_password):
                st.success("Login successful!")
                st.session_state['logged_in'] = True
                st.session_state['email'] = email
                st.experimental_rerun()  # Refresh the page after successful login
            else:
                st.error("Incorrect password")
        else:
            st.error("User not found")
        
        cursor.close()
        connection.close()

# Logout function
def logout():
    if st.button("Logout"):
        st.session_state.clear()  # Clear all session state
        st.experimental_rerun()  # Refresh the app to return to the login page

# Main function
# Main function
def main():
    st.title("Personal Finance Tracker")

    # Check if user is logged in
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    # If the user is logged in, show the main app with the menu and tools
    if st.session_state['logged_in']:
        st.sidebar.success(f"Logged in as {st.session_state['email']}")
        
        # Display app menu and tools
        menu = ["Home", "Transaction Tracking", "Budget Allocation", "Account Management", "Logout"]
        choice = st.sidebar.selectbox("Menu", menu)

        if choice == "Home":
            st.subheader("Welcome to the Personal Finance Tracker")
        elif choice == "Transaction Tracking":
            st.subheader("Transaction Tracking Page")
            # Add functionality for transaction tracking
        elif choice == "Budget Allocation":
            st.subheader("Budget Allocation Page")
            # Add functionality for budget allocation
        elif choice == "Account Management":
            st.subheader("Account Management Page")
            # Add functionality for account management
        elif choice == "Logout":
            st.session_state.clear()  # Clear all session state
            st.experimental_rerun()  # Refresh the app to return to the login page

    # If the user is not logged in, show login/signup options
    else:
        st.sidebar.title("Menu")
        choice = st.sidebar.selectbox("Menu", ["Login", "Sign Up"])

        if choice == "Login":
            login()  # Call the login function
        elif choice == "Sign Up":
            sign_up()  # Call the sign-up function

if __name__ == "__main__":
    main()

