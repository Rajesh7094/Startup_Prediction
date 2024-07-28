import streamlit as st
import pandas as pd
import subprocess
import openpyxl


# Function to create a signup form with additional fields
def signup():
    st.subheader("Sign Up")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0, max_value=150, step=1)
    sex = st.selectbox("Sex", ["Male", "Female", "Other"])
    working_status = st.selectbox("Working Status", ["Employed", "Unemployed", "Student", "Other"])
    company_name = st.text_input("Company Name")

    if st.button("Sign Up"):
        if password == confirm_password:
            if username not in df['Username'].values:
                # Add new user to the DataFrame
                new_user = pd.DataFrame({
                    'Username': [username],
                    'Password': [password],
                    'Name': [name],
                    'Age': [age],
                    'Sex': [sex],
                    'Working Status': [working_status],
                    'Company Name': [company_name]
                })
                # Append new user to the existing DataFrame
                updated_df = pd.concat([df, new_user], ignore_index=True)
                # Save the updated DataFrame to the Excel file
                updated_df.to_excel("user_credentials.xlsx", index=False, engine='xlsxwriter')
                st.success("Signed up successfully! Please log in.")
            else:
                st.warning("Username already exists. Please choose a different username.")
        else:
            st.warning("Passwords do not match. Please re-enter.")

def login():
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in df['Username'].values:
            stored_password = str(df.loc[df['Username'] == username, 'Password'].values[0])
            
            # Debug statements
            st.write(f"Entered password: {password}")
            st.write(f"Stored password: {stored_password}")

            if password.strip() == stored_password.strip():
                st.success(f"Welcome, {username}! You are logged in.")
                # Navigate to startup.py after successful login
                subprocess.run(["streamlit", "run", "startupda.py"])
            else:
                st.warning("Incorrect password. Please try again.")
        else:
            st.warning("Username not found. Please sign up.")

# Load existing user credentials from Excel file or create a new DataFrame if file doesn't exist
try:
    df = pd.read_excel("user_credentials.xlsx", engine='openpyxl')
except FileNotFoundError:
    df = pd.DataFrame(columns=['Username', 'Password', 'Name', 'Age', 'Sex', 'Working Status', 'Company Name'])

# Streamlit UI
st.title("Login and Sign Up")

# Sidebar navigation
page = st.sidebar.radio("Navigate", ("Login", "Sign Up"))

if page == "Login":
    login()
else:
    signup()
