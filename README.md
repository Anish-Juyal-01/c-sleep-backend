# C-Sleep Data Diagnostic API

This is the backend API for the C-Sleep Flutter application, built with FastAPI. It provides an endpoint to analyze sleep data from `.csv` or `.xlsx` files.

## Features

-   **File Upload**: Accepts `.csv` and `.xlsx` files.
-   **Data Validation**: Checks for required columns in the dataset.
-   **AI Analysis**: Uses Google's Gemini model via LangChain to compare user data against a baseline and generate a pre-diagnostic summary.

## Deployment on Render

This service is configured for easy deployment on Render.

1.  **Push to GitHub**: Push this repository to your GitHub account.
2.  **Connect to Render**:
    -   On the Render Dashboard, click **New +** and select **Blueprint Instance**.
    -   Connect the GitHub repository containing this code.
    -   Render will automatically detect the `render.yaml` file and configure the web service. Click **Approve**.
3.  **Add Environment Variable**:
    -   In the Render dashboard for your new service, go to the **Environment** tab.
    -   Under "Secret Files & Environment Groups", add a new Environment Variable:
        -   **Key**: `API_KEY`
        -   **Value**: Your actual Google AI Studio API key.

The service will automatically build and deploy. Your API will be live at the URL provided by Render.

## Local Development

1.  **Create a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Create a `.env` file** in this folder and add your API key:
    ```
    API_KEY="your_google_api_key_here"
    ```
4.  **Run the server**:
    ```bash
    uvicorn main:app --reload
    ```
The server will be running at `http://127.0.0.1:8000`.