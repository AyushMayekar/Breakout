# Importing Dependencies
import streamlit as st
import pandas as pd
from google.oauth2 import service_account
import gspread
from dotenv import load_dotenv
import os
import requests
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.schema import Document
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain


# Loading Credentials 
load_dotenv()
SERVICE_ACCOUNT_FILE = os.getenv('SERVICE_ACCOUNT_FILE')
SERPAPI_KEY = os.getenv('SERPAPI_KEY')
GROQ_API_KEY = os.environ['GROQ_API_KEY']
# print(SERVICE_ACCOUNT_FILE)


# rag integration
def rag_integration(query, gathered_data):
    try:
        # documenting the web search results
        documents = [
            Document(    page_content=f"{item['snippet']} (Link: {item['link']})", 
            metadata={"title": item["title"]})
            for item in gathered_data
            ]
    
        # initializing ollama embeddings
        embeddings = OllamaEmbeddings(model='nomic-embed-text')

        # storing data to the vector store
        vector_store = FAISS.from_documents(documents, embeddings)

        # Defining the LLM
        llm = ChatGroq(groq_api_key = GROQ_API_KEY, 
                    model_name = 'llama3-8b-8192')

        # Defining Prompt
        full_prompt = PromptTemplate.from_template(
            template="""Prompt:{input}\n\nHere is the relevant information gathered from the web:\n
                                            <Context>
                                            {context}
                                            </Context>\n\n
                                            Please provide a concise upto the mark (mostly a one word or number) answer based on the above prompt and provided information.""")

        # Creating a document chain
        doc_chain = create_stuff_documents_chain(llm = llm, prompt = full_prompt, output_parser= StrOutputParser())

        # Defining the vector store as retriever
        retriever = vector_store.as_retriever( search_type = "similarity",
        search_kwargs = { "k": 10 })

        # Creating a retrieval chain
        retrieval_chain = create_retrieval_chain(retriever, doc_chain)

        # invoking retrieval chain
        response = retrieval_chain.invoke({"input":query})

        return response['answer']
    except Exception as e:
        st.error(f"An error occurred during RAG integration: {str(e)}")
        return None

# Retrieve Web Data
def retrieve_web_data(query):
    try:
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
    except Exception as e :
        st.error(f"An error occurred during web data retrieval: {str(e)}")
        return None



# Implementing google sheet integration
def get_gspread_client():
    try:
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE,
            scopes=[
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive",
            ],
        )
        return gspread.authorize(credentials)
    except Exception as e :
        st.error(f"An error occurred during Google Sheets integration: {str(e)}")
        return None


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
        st.write("### Define Your Custom Prompt")
        st.write("Use `{object}` as a placeholder for the company name or selected entity(eg. country, website, animal, etc) in your prompt.")
        
        # Text input for custom prompt
        prompt = st.text_input(
                "Enter your custom prompt with placeholders.",
                placeholder="Get me the email address of {object}"
            )

        # Instructions  
        st.write("Example: `What continent does this {object} belong to? ` or `Find the location of {object}'s headquarters.`")
        
        if st.button("Process Prompt"):
            if prompt:
                with st.spinner("Processing..."):
                    gathered_data = []
                    llm_responses = [] 
                    for item in selected_data[selected_columns[0]].dropna().unique():
                        query = prompt.format(object = item)
                        results = retrieve_web_data(query)
                        gathered_data.extend(results)
                        llm_result = rag_integration(query, gathered_data)
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
        This tool is designed to make data analysis, information retrieval, and interaction with advanced language models seamless. 
        With this tool, you can upload datasets, retrieve valuable information from the web, and generate insights using RAG (Retrieval-Augmented Generation).
    """)

    # Walkthrough
    st.subheader("Step-by-Step Walkthrough")
    st.write("Here's how to get started with this tool:")

    # Step 1: Upload Data
    st.markdown("### 1. Uploading Your Data")
    st.write("""
        - Navigate to the **Playground** section.
        - **Upload a file**: Supported formats are **CSV** and **Excel (.xlsx)**. You can select specific sheets from Excel files.
        - **Connect Google Sheets**: Enter your Google Sheet's URL. Select the worksheet from the dropdown.
    """)

    # Step 2: Selecting Columns for Processing
    st.markdown("### 2. Selecting Columns for Processing")
    st.write("""
        - Once your file or Google Sheet is loaded, the data will be displayed.
        - Use the **column selection tool** to choose relevant columns for processing.
    """)

    # Step 3: Entering a Custom Prompt
    st.markdown("### 3. Entering a Prompt for Analysis")
    st.write("""
        - Enter a **custom prompt** in the provided input box. Use placeholders such as `{object}` to represent dynamic entities.
        - **Examples**:
            - "What is the headquarter location of {object}?"
            - "What continent does this {object} belong to?"
    """)

    # Step 4: Processing and Generating Results
    st.markdown("### 4. Processing and Generating Results")
    st.write("""
        - Click **"Process Prompt"** to retrieve data and generate insights.
        - The tool performs the following steps:
            - **Web Retrieval**: Fetches real-time information using **SerpAPI**.
            - **RAG Integration**: Stores data in a vector database using **FAISS** and generates responses using **ChatGroq**.
        - Results are displayed in a table format and can be downloaded as a CSV file.
    """)

    # Step 5: Downloading Results
    st.markdown("### 5. Downloading Results")
    st.write("""
        - After processing, use the **Download as CSV** button to save the results for external use.
    """)

    # Features and Functionalities
    st.subheader("Features and Functionalities")
    st.markdown("""
    - **Dynamic Prompt Creation**: Define custom prompts with placeholders for flexible queries.
    - **Real-Time Data Retrieval**: Fetch information directly from the web using **SerpAPI**.
    - **RAG Integration**: Combines vector store capabilities with LLMs for accurate and concise responses.
    - **Error Handling**: Built-in alerts for common issues like invalid URLs or failed API calls.
    """)

    # Technology Used
    st.subheader("Technologies Used")
    st.write("This tool leverages the following technologies:")
    st.markdown("""
    - **Streamlit**: For an interactive and user-friendly web interface.
    - **Pandas**: For data manipulation and visualization.
    - **Google Sheets API**: To fetch data from Google Sheets.
    - **SerpAPI**: For real-time web search and retrieval.
    - **LangChain**:
        - **Ollama Embeddings**: To encode text into high-dimensional vectors.
        - **FAISS**: For efficient similarity search on vectorized data.
        - **ChatGroq**: A powerful large language model for text generation and insights.
    """)

    # Industry Applications
    st.subheader("Industry Applications and Use Cases")
    st.write("""
        This tool is applicable across various domains, including:
    """)
    st.markdown("""
    1. **Market Research**: Retrieve real-time data on competitors, trends, and insights.
    2. **Customer Insights**: Analyze customer reviews, public sentiment, and feedback.
    3. **Recruitment**: Gather company-related data like employee size and headquarters location.
    4. **Data Enrichment**: Augment datasets with web-sourced information for richer context.
    """)

    # Support and Resources
    st.subheader("Support and Resources")
    st.write("Need help? Refer to the following resources or use the **Contact Us** section:")
    st.markdown("""
    - **[SerpAPI Documentation](https://serpapi.com/)**: Learn about the web search API.
    - **[Google Sheets API Guide](https://developers.google.com/sheets/api/guides/concepts)**: For integrating Google Sheets.
    - **[Streamlit Documentation](https://docs.streamlit.io/)**: For creating interactive web applications.
    """)

    # Closing Remark
    st.write("We hope this guide helps you get the most out of the tool. Happy analyzing! 🎉")


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
st.sidebar.title("🧭 Navigation")

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