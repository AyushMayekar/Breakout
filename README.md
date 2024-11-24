# Data Insight and Analysis Tool

## Project Description

This tool is designed to streamline data analysis and insights generation by integrating data from user-uploaded files (CSV, Excel) or Google Sheets with powerful web data retrieval and Retrieval-Augmented Generation (RAG) using language models (LLMs). It allows users to dynamically retrieve information from the web, process this data with the Llama3 language model, and export structured insights. With features like error handling and custom prompts, this tool is ideal for use cases such as market research, customer analysis, human resources, and data enrichment.

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/AyushMayekar/Data_Insight_and_Analysis_Tool
```

### 2. Install Dependencies

Use the `requirements.txt` file to install all necessary dependencies:
```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

Create a `.env` file in the root of the project folder and enter your API keys and required configurations:
```plaintext
GROQ_API_KEY=your_groq_api_key
SERVICE_ACCOUNT_FILE=path/to/your-google-service-account.json
SERPAPI_KEY=your_serpapi_key
```

- **GROQ_API_KEY**: API key for the Groq platform to use the Llama3 language model.
- **SERVICE_ACCOUNT_FILE**: Path to the Google service account JSON file for accessing Google Sheets.
- **SERPAPI_KEY**: API key for SerpAPI, used for web scraping.

### 4. Run the Application

Start the Streamlit application with the following command:
```bash
streamlit run main.py
```

---

## Usage Guide

This tool provides an interactive interface for uploading or connecting data sources, selecting relevant data, running analysis, and exporting results.

### 1. Uploading Data

In the **Playground** section:
- **Choose a file** to upload (supported formats: CSV, Excel).
  - For Excel files, select the desired sheet from the dropdown.
- **Or connect to a Google Sheet**:
  - Enter the Google Sheet URL to import data directly from Google Sheets.
  - Ensure your Google account has permissions to access the sheet.

### 2. Selecting Columns for Analysis

After uploading data:
- Select specific columns for processing by using the **column selector**.
- This allows you to target specific data points for retrieval and analysis.

### 3. Entering a Custom Prompt

Once columns are selected:
- Enter a custom prompt in the provided text input box. Use placeholders like `{object}` to represent dynamic entities (e.g., company, website, or location).
- **Examples**:
  - "What is the headquarters location of {object}?"
  - "What continent does this {object} belong to?"

### 4. Processing and Reviewing Results

After defining your prompt:
- Click **Process Prompt** to retrieve and process data using:
  - **Web Retrieval**: Fetches real-time information from SerpAPI.
  - **RAG Integration**: Uses FAISS for vector search and Llama3 for generating insights.
- Review results in a structured table format.

### 5. Exporting Results

Use the **Download as CSV** button to save the generated results for further use.

---

## Screenshots

1. Data Insight and Analysis Tool Interface Example:

![1](https://github.com/AyushMayekar/Breakout/blob/main/playground_ss.png)

2. Data Insight and Analysis Tool Interface Example:

![2](https://github.com/AyushMayekar/Breakout/blob/main/Guide_ss.png)

---

## Video Walkthrough

[![Watch the video](https://img.youtube.com/vi/vBYs6UqH4R4/maxresdefault.jpg)](https://youtu.be/vBYs6UqH4R4)
---

## API Keys and Environment Variables

To use this tool, you’ll need API keys and other environment variables stored in a `.env` file:

- **GROQ_API_KEY**: Required for using the Llama3 language model on Groq ([GROQ API Documentation](https://console.groq.com/keys)).
- **SERVICE_ACCOUNT_FILE**: Path to the JSON file for your Google Service Account credentials to access Google Sheets ([Google Sheets API Guide](https://developers.google.com/sheets/api/guides/concepts)).
- **SERPAPI_KEY**: Required for SerpAPI, enabling the tool to retrieve relevant web data based on user queries ([SerpAPI Documentation](https://serpapi.com/)).

### Example `.env` file
```plaintext
GROQ_API_KEY=your_groq_api_key
SERVICE_ACCOUNT_FILE=path/to/your-google-service-account.json
SERPAPI_KEY=your_serpapi_key
```

---

## Features

### Key Features
- **Dynamic Prompt Creation**: Users can define prompts with placeholders for flexible and customized queries.
- **Real-Time Data Retrieval**: Fetch information directly from the web using SerpAPI.
- **RAG Integration**: Combines FAISS and Llama3 for accurate and concise insights.
- **Error Handling**: Provides user-friendly alerts for common issues.
- **Downloadable Results**: Export analysis and insights in CSV format.

### Optional Features
- **Dynamic Sheet Selection**: Choose specific sheets from uploaded Excel files.
- **Customizable Prompts**: Tailor queries dynamically using placeholders.
- **Responsive Sidebar Navigation**: Quickly switch between sections using an intuitive sidebar.
- **Modular Design**: Easily extend or modify functionalities.

---

## How This Tool is Useful for the Industry

This tool is built to address real-world use cases across industries:

1. **Market Research**: Analyze competitors and track industry trends.
2. **Customer Analysis**: Gather sentiment analysis, reviews, and customer engagement data.
3. **Human Resources**: Fetch employee data and company profiles for recruitment or collaboration.
4. **Data Enrichment**: Enhance raw datasets with additional contextual information.

---

## Support and Resources

For further information, refer to these resources:
- **[SerpAPI Documentation](https://serpapi.com/)**: Learn more about web search API usage.
- **[Google Sheets API Guide](https://developers.google.com/sheets/api/guides/concepts)**: Help with setting up Google Sheets integration.
- **[Streamlit Documentation](https://docs.streamlit.io/)**: Build interactive and dynamic web applications.

---

## Contact

For further information about this tool, please reach out to the project creator via [LinkedIn](https://www.linkedin.com/in/ayush-mayekar-b9b883284).

---

Thank you for using the **Data Insight and Analysis Tool**! We hope it simplifies your workflow and enhances your data analysis experience. 🎉
