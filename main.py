# Importing Dependencies
import streamlit as st
import pandas as pd
from google.oauth2 import service_account
import gspread
from dotenv import load_dotenv
import os
import requests
from groq import Groq

# Loading Credentials 
load_dotenv()
SERVICE_ACCOUNT_FILE = os.getenv('SERVICE_ACCOUNT_FILE')
SERPAPI_KEY = os.getenv('SERPAPI_KEY')
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)
# print(SERVICE_ACCOUNT_FILE)


# LLM integration 
def llm_integration(prompt, gathered_data) :
    # Merging all the web scraped data
    data_summary = "\n".join([f"{item['title']}: {item['snippet']} (Link: {item['link']})" for item in gathered_data])

    # Create a structured prompt for the LLM
    full_prompt = f"Prompt:{prompt}\n\nHere is the relevant information gathered from the web:\n{data_summary}\n\nPlease provide a concise upto the mark (mostly a one word or number) answer based on the above prompt and provided information."
    
    try:
        # Send prompt to OpenAI's API and get a response
        response = client.chat.completions.create(
            messages=[
        {
            "role": "user",
            "content": full_prompt,
        }
        ],
        model="llama3-8b-8192"
        )
        
        # Extract the response text
        answer = response.choices[0].message.content
        return answer
    except Exception as e:
        return f"Error processing with LLM: {e}"

# Retrieve Web Data
def retrieve_web_data(query):
    url = f"https://serpapi.com/search.json"
    params = {
        "q": query,
        "api_key": SERPAPI_KEY,
        "num": 3
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
    st.title("🎮 Playground")
    st.write("Upload a file or connect your google sheet to begin.")

    # List to store selected columns 
    selected_columns = []

    # File uploader
    uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx"])

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
            sheet_names = pd.ExcelFile(uploaded_file).sheet_names
            sheet = st.selectbox("Select a sheet", sheet_names)
            # Load the selected sheet
            df = pd.read_excel(uploaded_file, sheet_name=sheet)
            st.write("File content:")
            st.dataframe(df)
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
        prompt = st.text_area("Describe what you want to do with the selected columns.", height=150, placeholder='Eg. Find the company size of given company, Find me the exact location of the company headquaters...')
        
        if st.button("Process Prompt"):
            if prompt:
                with st.spinner("Processing..."):
                    gathered_data = []
                    llm_responses = [] 
                    for item in selected_data[selected_columns[0]].dropna().unique():
                        query = f"{item}: {prompt}"
                        results = retrieve_web_data(query)
                        gathered_data.extend(results)
                        llm_result = llm_integration(query, gathered_data)
                        llm_responses.append({"Company": item, prompt: llm_result})
                    result_data = pd.DataFrame(llm_responses)
                    st.write("### LLM Results")

                    # Add download button for CSV
                    csv = result_data.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="Download results as CSV",
                        data=csv,
                        file_name="llm_results.csv",
                        mime="text/csv",
                    )
                    st.dataframe(result_data)
            else:
                st.warning("Please enter a prompt to proceed.")
                



# Guide Page
def guide():
    st.title("📘 Guide")

    # Introduction
    st.subheader("Welcome to the Tool Guide")
    st.write("""
        This tool is designed to make data analysis, information retrieval, and language model (LLM) interaction seamless. 
        With this tool, you can easily upload datasets, retrieve valuable information from the web, and generate insights using advanced LLMs.
    """)

    # Walkthrough
    st.subheader("Step-by-Step Walkthrough")
    st.write("Here's how to get started with this tool:")

    # Step 1: Upload Data
    st.markdown("### 1. Uploading Your Data")
    st.write("""
        - Go to the **Playground** section.
        - Choose a file to upload by clicking the **'Choose a file'** button. Supported file formats include:
            - **CSV**: Comma-separated values, a standard format for data files.
            - **Excel (.xlsx)**: Allows selecting a specific worksheet.
        - Or, connect your **Google Sheet** by entering its URL in the provided field.
    """)

    # Step 2: Selecting Columns
    st.markdown("### 2. Selecting Columns for Processing")
    st.write("""
        - Once your file is uploaded or Google Sheet is connected, you’ll see your data displayed.
        - Use the **column selection tool** to choose specific columns for further processing. 
        - This step helps you focus on the relevant data points, saving time and improving accuracy in subsequent steps.
    """)

    # Step 3: Entering a Prompt
    st.markdown("### 3. Entering a Prompt for Analysis")
    st.write("""
        - After selecting columns, you’ll see a **text input area** to enter a prompt.
        - This prompt directs the tool on what information to retrieve from the web or analyze using the LLM.
        - Examples of prompts:
            - "Find the headquarter location of each company."
            - "Get the latest news related to each listed company."
            - "Fetch employee count or company size for each company."
    """)

    # Step 4: Processing Prompt and Generating Results
    st.markdown("### 4. Processing and Retrieving Results")
    st.write("""
        - Click on **'Process Prompt'** to start the information retrieval process.
        - The tool will retrieve data from the web based on your prompt and apply the LLM to get precise, actionable answers.
        - The results will be displayed in a structured format and include a **Download as CSV** option for easy export.
    """)

    # Step 5: Downloading the Results
    st.markdown("### 5. Downloading Results")
    st.write("""
        - After results are generated, use the **Download button** to save the insights as a CSV file.
        - This file will include the original data and the generated insights, which you can integrate into further analysis or reports.
    """)

    # Features and Functionalities
    st.subheader("Features and Functionalities")
    st.markdown("""
    - **Data Upload and Integration**: Upload CSV or Excel files or link to a Google Sheet for seamless data access.
    - **Customizable Analysis**: Select specific columns and enter targeted prompts to obtain tailored insights.
    - **Web Data Retrieval**: Uses SerpAPI to pull information from the web based on user queries.
    - **LLM Integration**: Integrates with a powerful LLM (Llama3) to generate concise, precise answers based on web-scraped data.
    - **Downloadable Results**: Export analysis as a CSV file for easy integration with other tools.
    """)

    # Technology Used
    st.subheader("Technologies Used")
    st.write("This tool leverages cutting-edge technologies to deliver a smooth, effective experience:")
    st.markdown("""
    - **Streamlit**: A powerful framework for building interactive web applications in Python.
    - **Pandas**: For data manipulation, reading, and structuring CSV and Excel files.
    - **Google Sheets API**: For integrating Google Sheets as an alternative to CSV and Excel.
    - **SerpAPI**: For real-time web data retrieval based on user queries.
    - **Groq and Llama3 Model**: A large language model for analyzing data and generating insights based on custom prompts.
    """)

    # How This Tool is Useful in the Industry
    st.subheader("Industry Applications and Use Cases")
    st.write("""
        This tool is versatile and can be applied across various industries for data analysis and insight generation. Some potential applications include:
    """)
    st.markdown("""
    - **Market Research**: Retrieve and analyze competitor information, trends, and insights in a structured format.
    - **Customer Analysis**: Quickly gather customer reviews, engagement data, and public sentiment for listed companies.
    - **Human Resources**: Analyze employee-related data such as company size or headquarter locations for potential recruiting or partnerships.
    - **Data Enrichment**: Use the tool to enrich raw data with web-sourced information, providing added context to datasets.
    """)

    # Support Section
    st.subheader("Support and Resources")
    st.write("Need help? Contact us through the **Contact Us** page or refer to the following resources:")
    st.markdown("""
    - **SerpAPI Documentation**: For details on the web scraping capabilities, see the [SerpAPI documentation](https://serpapi.com/).
    - **Google Sheets API Guide**: Learn how to integrate Google Sheets [here](https://developers.google.com/sheets/api/guides/concepts).
    - **Streamlit Guide**: For more information on Streamlit features, see the [Streamlit documentation](https://docs.streamlit.io/).
    """)

    # Closing Remark
    st.write("We hope this guide helps you get the most out of the tool. Happy analyzing!")


# Contact Us Page
def contact():
    st.title("📧 Contact Us")
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



# Sidebar
st.sidebar.title("Navigation")

if "page" not in st.session_state:
    st.session_state["page"] = "Guide"  # Default page
if st.sidebar.button("🎮 Playground"):
    st.session_state["page"] = "Playground"
if st.sidebar.button("📘 Guide"):
    st.session_state["page"] = "Guide"
if st.sidebar.button("📧 Contact Us"):
    st.session_state["page"] = "Contact Us"

# Page selection based on session state
if st.session_state["page"] == "Playground":
    playground()
elif st.session_state["page"] == "Guide":
    guide()
elif st.session_state["page"] == "Contact Us":
    contact()