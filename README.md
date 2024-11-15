# Data Insight and Analysis Tool

## Project Description

This tool is designed to streamline data analysis and insights generation by integrating data from user-uploaded files (CSV, Excel) or Google Sheets with powerful web data retrieval and language model (LLM) analysis capabilities. It enables users to retrieve relevant information from the web, process this data with the Llama3 language model, and export structured insights. This tool is particularly useful for market research, customer analysis, human resources, and data enrichment, allowing users to gain valuable insights with ease.

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-folder>
```

### 2. Create and Activate a Virtual Environment (Optional but Recommended)

For Python 3:
```bash
python3 -m venv env
source env/bin/activate   # For Unix/Mac
env\Scripts\activate      # For Windows
```

### 3. Install Dependencies

Use the `requirements.txt` file to install all necessary dependencies:
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the root of the project folder and enter your API keys and required configurations:
```plaintext
GROQ_API_KEY=your_groq_api_key
SERVICE_ACCOUNT_FILE=path/to/your-google-service-account.json
SERPAPI_KEY=your_serpapi_key
```

- **GROQ_API_KEY**: API key for the Groq platform to use the Llama3 language model.
- **SERVICE_ACCOUNT_FILE**: Path to the Google service account JSON file for accessing Google Sheets.
- **SERPAPI_KEY**: API key for SerpAPI, used for web scraping.

### 5. Run the Application

Start the Streamlit application with the following command:
```bash
streamlit run app.py
```

---

## Usage Guide

This tool provides an interactive interface that allows users to upload or connect data sources, select relevant data, run analysis, and export results.

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

### 3. Entering a Prompt for Data Retrieval

Once columns are selected:
- Enter a prompt in the **text area** to specify the type of information you’re looking to retrieve.
  - Examples of prompts:
    - "Find the company headquarters location."
    - "Retrieve the company size for each listed company."
- Click **Process Prompt** to retrieve data from the web based on the prompt.

### 4. Reviewing Results and Exporting Data

After processing:
- The tool displays the gathered data and LLM-generated responses in a table format.
- Use the **Download as CSV** button to export the results for further analysis.

---

## API Keys and Environment Variables

To use this tool, you’ll need API keys and other environment variables stored in a `.env` file:

- **GROQ_API_KEY**: Required for using the Llama3 language model on Groq [GROQ API KEY DOCUMENTATION](https://console.groq.com/keys).
- **SERVICE_ACCOUNT_FILE**: Path to the JSON file for your Google Service Account credentials to access Google Sheets [GOOGLE SHEETS GUIDE](https://developers.google.com/sheets/api/guides/values).
- **SERPAPI_KEY**: Required for SerpAPI, enabling the tool to retrieve relevant web data based on user queries  [SerpAPI DOCUMENTATION](https://serpapi.com/).

### Example `.env` file
```plaintext
GROQ_API_KEY=your_groq_api_key
SERVICE_ACCOUNT_FILE=path/to/your-google-service-account.json
SERPAPI_KEY=your_serpapi_key
```

Ensure that each key is set up correctly and that your `.env` file is in the root directory of your project.

---

## Screenshots

1. Data Insight and Analysis Tool Interface Example:

![1](https://github.com/AyushMayekar/Breakout/blob/main/playground_ss.png)

2. Data Insight and Analysis Tool Interface Example:

![2](https://github.com/AyushMayekar/Breakout/blob/main/Guide_ss.png)

---

## Video Walkthrough

here 

---

## Optional Features

This tool includes several additional features to enhance its functionality and user experience:

- **Dynamic Sheet Selection**: For Excel files, users can select a specific sheet to load, allowing for flexibility in data selection.
- **Customizable Prompts**: Users can specify custom prompts for each analysis, allowing for targeted data retrieval and customized responses from the LLM.
- **Export Functionality**: Results are easily exportable as a CSV file, enabling users to integrate the generated insights with other tools.
- **Responsive Sidebar Navigation**: Attractive sidebar navigation with icons allows for easy navigation between different sections of the tool.
- **Modular Design**: The application follows a modular structure, making it easy to add new features or modify existing ones.

---

## How This Tool is Useful for the Industry

This tool is designed with flexibility and functionality to address real-world use cases, making it a valuable asset across multiple industries:

- **Market Research**: Quickly gather and analyze competitor information or industry trends.
- **Customer Analysis**: Gather sentiment analysis, reviews, and customer engagement data.
- **Human Resources**: Fetch employee information or company size to identify potential partnerships.
- **Data Enrichment**: Enhance existing datasets with up-to-date information retrieved from the web.

With its robust integrations and customizable prompts, this tool simplifies the process of turning raw data into actionable insights.

---

## Contact

For further information about my tool, please reach out to the project creator via [LinkedIn](https://www.linkedin.com/in/ayush-mayekar-b9b883284).

---

Thank you for your interest and valuable time. 🤝
We hope you enjoy using this tool and find it useful for your data analysis needs!!