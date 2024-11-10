# Importing Dependencies
import streamlit as st
import pandas as pd
from google.oauth2 import service_account
import gspread
from dotenv import load_dotenv
import os
import requests

# Loading Credentials 
load_dotenv()
SERVICE_ACCOUNT_FILE = os.getenv('SERVICE_ACCOUNT_FILE')
SERPAPI_KEY = os.getenv('SERPAPI_KEY')
# print(SERVICE_ACCOUNT_FILE)


# Retrieve Web Data
def retrieve_web_data(query):
    url = f"https://serpapi.com/search.json"
    params = {
        "q": query,
        "api_key": SERPAPI_KEY,
        "num": 2
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("organic_results", [])
    else:
        return f"Error retrieving data: {response.status_code}"

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

    # List to store selected columns 
    selected_columns = []

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
            if data:
                df = pd.DataFrame(data)
                st.write("Data from Google Sheet:")
                st.dataframe(df)
                selected_columns = st.multiselect("Select columns for processing", options=df.columns.tolist())
                if selected_columns:
                    st.write("Selected columns for further processing:")
                    selected_data = df[selected_columns]
                    st.dataframe(selected_data)
            else:
                st.warning("The selected worksheet is empty.")

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
        if 'df' in locals():
            selected_columns = st.multiselect("Select columns for processing", options=df.columns.tolist())
            if selected_columns:
                st.write("Selected columns for further processing:")
                selected_data = df[selected_columns]
                st.dataframe(selected_data)
        else:
            st.warning("Unsupported file format.")

    if selected_columns:
        st.write("### Enter Your Prompt")
        prompt = st.text_area("Describe what you want to do with the selected columns.", height=150, placeholder='Eg. Fetch Email, find location, find colour...')
        
        if st.button("Process Prompt"):
            if prompt:
                with st.spinner("Processing..."):
                    gathered_data = []
                    for item in selected_data[selected_columns[0]].dropna().unique():
                        query = f"{prompt} for {item}"
                        results = retrieve_web_data(query)
                        gathered_data.extend(results)
                    
                    # Display gathered results
                    if gathered_data:
                        st.write("### Gathered Web Information")
                        for idx, result in enumerate(gathered_data, start=1):
                            st.write(f"**{idx}. {result.get('title')}**")
                            st.write(result.get('snippet'))
                            st.write(f"Link: {result.get('link')}\n")
            else:
                st.warning("Please enter a prompt to proceed.")


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