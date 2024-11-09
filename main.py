# Importing Dependencies
import streamlit as st
import pandas as pd
from google.oauth2 import service_account
import gspread
from dotenv import load_dotenv
import os


load_dotenv()
SERVICE_ACCOUNT_FILE = os.getenv('SERVICE_ACCOUNT_FILE')
# print(SERVICE_ACCOUNT_FILE)

# Implementing google sheet integration
def get_gspread_client():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=[
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ],
    )
    return gspread.authorize(credentials)


# Main Logic Page
def playground():
    st.title("Playground")
    st.write("Upload a file or connect your google sheet to begin.")

    # File uploader
    uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx", "txt"])

    # Google Sheets selection
    st.write("Or connect to a Google Sheet:")
    
    # Prompt for Google Sheets URL
    sheet_url = st.text_input("Enter Google Sheets URL")
    if sheet_url:
        try:
            # Initialize Google Sheets client
            client = get_gspread_client()
            # Open the Google Sheet by URL
            sheet = client.open_by_url(sheet_url)
            # Get list of worksheets (tabs) in the Google Sheet
            worksheet_list = [ws.title for ws in sheet.worksheets()]
            
            # Select a worksheet from a dropdown
            worksheet_name = st.selectbox("Select Worksheet", worksheet_list)
            worksheet = sheet.worksheet(worksheet_name)
            # Get all records from the selected worksheet as a DataFrame
            data = worksheet.get_all_records()
            df = pd.DataFrame(data)
            
            # Display data in the app
            st.write("Data from Google Sheet:")
            st.dataframe(df)
        except Exception as e:
            st.error(f"Error loading Google Sheet: {e}")

    
    # Display file content or provide feedback
    if uploaded_file is not None:
        st.success("File uploaded successfully!")
        
        # Display the file contents for CSV and text files
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
            st.write("File content:")
            st.dataframe(df)
        elif uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
            st.write("File content:")
            st.dataframe(df)
        elif uploaded_file.name.endswith('.txt'):
            text = uploaded_file.read().decode("utf-8")
            st.write("File content:")
            st.text(text)
        else:
            st.warning("Unsupported file format.")


# Guide Page
def guide():
    st.title("Guide")
    st.write("""
    ## How to Use the App
    - **Playground**: Upload your file here to test functionality.
    - **Guide**: This page provides information on how to use the app.
    - **Contact Us**: Reach out to us for support or inquiries.
    
    ## Supported File Types
    - CSV files (.csv)
    - Excel files (.xlsx)
    - Text files (.txt)
    """)
    st.info("For detailed instructions, please refer to the documentation or contact support.")


# Contact Us Page
def contact():
    st.title("Contact Us")
    st.write("We would love to hear from you!")

    # Contact form
    with st.form("contact_form"):
        name = st.text_input("Your Name")
        email = st.text_input("Your Email")
        message = st.text_area("Your Message")
        
        # Submit button
        submitted = st.form_submit_button("Send Message")
        if submitted:
            st.success("Your message has been sent!")
            st.write(f"**Name:** {name}")
            st.write(f"**Email:** {email}")
            st.write(f"**Message:** {message}")


# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ("Playground", "Guide", "Contact Us"))

# Page selection
if page == "Playground":
    playground()
elif page == "Guide":
    guide()
elif page == "Contact Us":
    contact()