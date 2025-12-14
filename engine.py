import google.generativeai as genai
import streamlit as st
import os

def generate_question(previous_answer: str, resume_data: str, api_key: str) -> str:
    """
    Generate a follow-up interview question based on the candidate's previous answer and resume data.
    """
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        
        prompt = f"""
        You're a professional interviewer. Ask a follow-up question based on the candidate's previous answer and resume details.
        
        Resume: {resume_data}
        Candidate's answer: {previous_answer}
        
        Generate only the question.
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"🚨 API Error: {str(e)}"

def generate_feedback(answer: str, api_key: str) -> str:
    """
    Generate feedback on the candidate's answer.
    """
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        
        prompt = f"""
        You're an AI interviewer who provides constructive feedback.
        Please evaluate and provide feedback on the following candidate answer: {answer}
        
        Keep it concise and constructive.
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"🚨 API Error: {str(e)}"
