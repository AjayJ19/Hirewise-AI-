import requests

import streamlit as st
import os

# Try to get key from Streamlit secrets, otherwise fallback to environment or hardcoded
DEFAULT_KEY = "3cqS6ejaXUrBGUOsHyId1xCVRkm5OOrN"
try:
    MISTRAL_API_KEY = st.secrets["MISTRAL_API_KEY"]
except:
    # Fallback for local testing if secrets.toml doesn't exist
    MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY", DEFAULT_KEY)

if MISTRAL_API_KEY == DEFAULT_KEY:
    st.warning("⚠️ You are using the default invalid API key. Please configure 'MISTRAL_API_KEY' in Streamlit Secrets.")

MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"

def generate_question(previous_answer: str, resume_data: str) -> str:
    """
    Generate a follow-up interview question based on the candidate's previous answer and resume data.
    """
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "open-mistral-7b",  # Changed to free/open model
        "messages": [
            {"role": "system", "content": "You're a professional interviewer. Ask a follow-up question based on the candidate's previous answer and resume details."},
            {"role": "user", "content": f"Candidate's answer: {previous_answer}\nResume: {resume_data}"}
        ],
        "max_tokens": 200
    }
    
    response = requests.post(MISTRAL_API_URL, json=data, headers=headers, timeout=60)
    if response.status_code == 401:
        st.error("🚨 Authentication Failed! Please add your 'MISTRAL_API_KEY' in Streamlit Secrets.")
        st.stop()
    elif response.status_code != 200:
        st.error(f"API Error: {response.status_code} - {response.text}")
        
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

def generate_feedback(answer: str) -> str:
    """
    Generate feedback on the candidate's answer.
    """
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "open-mistral-7b", # Changed to free/open model
        "messages": [
            {"role": "system", "content": "You're an AI interviewer who provides constructive feedback."},
            {"role": "user", "content": f"Please evaluate and provide feedback on the following candidate answer: {answer}"}
        ],
        "max_tokens": 200
    }
    
    response = requests.post(MISTRAL_API_URL, json=data, headers=headers, timeout=60)
    if response.status_code == 401:
        st.error("🚨 Authentication Failed! Please add your 'MISTRAL_API_KEY' in Streamlit Secrets.")
        st.stop()
    elif response.status_code != 200:
        st.error(f"API Error: {response.status_code} - {response.text}")
        
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

# Optional test when running the module directly
if __name__ == "__main__":
    # Test generate_question
    test_question = generate_question("I have 5 years of experience as a software engineer.", "John Doe's resume: Experienced in Python, JavaScript, and cloud computing.")
    print("Generated Question:", test_question)
    
    # Test generate_feedback
    test_feedback = generate_feedback("I managed to implement several features under tight deadlines.")
    print("Generated Feedback:", test_feedback)
