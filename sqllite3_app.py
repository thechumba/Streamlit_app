import streamlit as st
import sqlite3
import pandas as pd

# Initialize connection to SQLite
# Will create the database if it doesn't exist
conn = sqlite3.connect('data.db', check_same_thread=False)
c = conn.cursor()

# Create table if it doesn't exist
def init_db():
    c.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            notes TEXT
        )
    ''')
    conn.commit()

# Function to add a new record
def add_record(name, email, phone, notes):
    c.execute('''
        INSERT INTO contacts (name, email, phone, notes)
        VALUES (?, ?, ?, ?)
    ''', (name, email, phone, notes))
    conn.commit()

# Function to view all records
def view_records():
    df = pd.read_sql_query("SELECT * FROM contacts", conn)
    return df

# Initialize the database
init_db()

# Streamlit UI
st.title('Contact Manager')

# Form for adding new contacts
with st.form("contact_form"):
    st.write("Add New Contact")
    name = st.text_input("Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone")
    notes = st.text_area("Notes")
    
    submitted = st.form_submit_button("Save Contact")
    if submitted:
        if name:  # Basic validation
            add_record(name, email, phone, notes)
            st.success("Contact saved!")
        else:
            st.error("Name is required!")

# View existing records
st.write("## Existing Contacts")
if st.button("Refresh Data"):
    st.experimental_rerun()

# Display records in a table
records = view_records()
if not records.empty:
    st.dataframe(records)
else:
    st.write("No records found.")

# Clean up
def cleanup():
    conn.close()

# Register the cleanup function
import atexit
atexit.register(cleanup)