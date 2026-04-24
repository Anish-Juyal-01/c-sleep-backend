from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import List
import pandas as pd
import io
import os
from dotenv import load_dotenv

# LangChain imports (Mocked setup for production readiness)
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

app = FastAPI(title="C-Sleep Data Diagnostic API")

# Load environment variables from the .env file
load_dotenv()

class ConsultationResponse(BaseModel):
    analysis: str

# Mock baseline data representing 100,000 users
BASELINE_DATA = {
    "sleep_duration_hrs": 7.2,
    "sleep_quality_score": 75.0,
    "rem_percentage": 22.0,
    "deep_sleep_percentage": 18.0,
    "sleep_latency_mins": 15.0,
    "stress_score": 40.0
}

# Root endpoint for health checks
@app.get("/")
def read_root():
    return {"status": "C-Sleep API is running"}

@app.post("/analyze-sleep", response_model=ConsultationResponse)
async def analyze_consultation(file: UploadFile = File(...)):
    if not file.filename.endswith(('.csv', '.xlsx')):
        raise HTTPException(status_code=400, detail="Only .csv and .xlsx files are supported.")

    try:
        contents = await file.read()
        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(contents))
        else:
            df = pd.read_excel(io.BytesIO(contents))
        
        required_cols = ['sleep_duration_hrs', 'sleep_quality_score', 'rem_percentage', 'deep_sleep_percentage', 'sleep_latency_mins', 'stress_score']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            raise HTTPException(status_code=400, detail=f"Dataset is missing required columns: {missing_cols}")
        
        user_averages = df[required_cols].mean().to_dict()

        prompt_template = """
        You are an expert AI medical assistant for the C-Sleep app. Your goal is to prepare a 
        pre-diagnosis summary for a human doctor based purely on numerical data deviations.

        BASELINE AVERAGES (100,000 Users):
        {baseline_data}

        PATIENT AVERAGES (Uploaded Dataset):
        {user_data}

        Analyze ONLY the numerical deviations between the user's data and the baseline.
        Please provide:
        1. A Pre-Diagnosis Summary explaining the potential clinical meaning of these deviations.
        2. A list of 3 Actionable Questions the doctor should ask the patient.
        """
        
        # --- REAL GEMINI LLM INTEGRATION ---
        prompt = PromptTemplate.from_template(prompt_template)
        
        api_key = os.getenv("API_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="API Key is missing from the environment variables.")
        
        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.0, google_api_key=api_key, max_retries=1)
        chain = prompt | llm
        
        ai_response = chain.invoke({
            "baseline_data": BASELINE_DATA,
            "user_data": user_averages
        })
        raw_result = ai_response.content

        return ConsultationResponse(analysis=raw_result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))