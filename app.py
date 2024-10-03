import streamlit as st
from streamlit_option_menu import option_menu

# Set page config
st.set_page_config(page_title="Personal Finance Tracker", layout="wide")

# Custom CSS
st.markdown(
    """
    <style>
    .nav-bar {
        background-color: #f8f9fa; /* Background color for the nav bar */
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Navigation Menu
with st.container():
    selected = option_menu(
        menu_title=None,
        options=["Home", "Add Transactions", "Transaction History","Stats", "Budget", "Account Balance", "Settings", "Help"],
        icons=["house", "plus-circle", "list", "bar-chart", "wallet", "gear", "info-circle"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
    )

# Load the respective page
if selected == "Home":
    st.title("Welcome to Your Personal Finance Tracker")
    st.write("Overview and statistics will be displayed here.")
    # You can call your overview function here

elif selected == "Add Transactions":
    import pages.add_transaction as add_transaction
    add_transaction.run()

elif selected == "stats":
    import pages.statistics as statistics
    statistics.run()
    
elif selected == "Transaction History":
    import pages.transaction_history as transaction_history
    transaction_history.run()

elif selected == "Budget":
    import pages.budget as budget
    budget.run()

elif selected == "Account Balance":
    import pages.account_balance as account_balance
    account_balance.run()

elif selected == "Settings":
    import pages.settings as settings
    settings.run()

elif selected == "Help":
    import pages.help as help_page
    help_page.run()
