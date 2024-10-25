import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import os

# Create a SQLite database connection
DATABASE_URL = 'sqlite:///data.db'
engine = create_engine(DATABASE_URL)

# Function to save data to the database
def save_to_db(data):
    with engine.connect() as conn:
        # Create table if it doesn't exist
        conn.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT,
                age INTEGER
            )
        """)
        # Insert data into the table
        conn.execute("""
            INSERT INTO user_data (name, email, age) VALUES (?, ?, ?)
        """, (data['name'], data['email'], data['age']))

# Function to save data to a CSV file
def save_to_csv(data):
    csv_file = 'ihub.csv'
    # Check if the CSV file exists
    if os.path.exists(csv_file):
        # Append to the existing CSV file
        df = pd.read_csv(csv_file)
        df = df.append(data, ignore_index=True)
    else:
        # Create a new DataFrame and save it
        df = pd.DataFrame([data])
    
    df.to_csv(csv_file, index=False)

# Streamlit form
st.title('User  Data Form')

with st.form(key='user_form'):
    name = st.text_input('Name')
    email = st.text_input('Email')
    age = st.number_input('Age', min_value=0, max_value=120)
    
    submit_button = st.form_submit_button(label='Submit')

    if submit_button:
        # Create a dictionary with the form data
        data = {
            'name': name,
            'email': email,
            'age': age
        }
        # Save the data to the database
        save_to_db(data)
        # Save the data to a CSV file
        save_to_csv(data)
        st.success('Data saved to the database and CSV file successfully!')
