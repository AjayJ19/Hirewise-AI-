import requests

# Replace with your actual Mistral API key
MISTRAL_API_KEY = "3cqS6ejaXUrBGUOsHyId1xCVRkm5OOrN"
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
        "model": "mistral-medium",  # or another valid model if available
        "messages": [
            {"role": "system", "content": "You're a professional interviewer. Ask a follow-up question based on the candidate's previous answer and resume details."},
            {"role": "user", "content": f"Candidate's answer: {previous_answer}\nResume: {resume_data}"}
        ],
        "max_tokens": 200
    }
    
    response = requests.post(MISTRAL_API_URL, json=data, headers=headers, timeout=60)
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
        "model": "mistral-medium",
        "messages": [
            {"role": "system", "content": "You're an AI interviewer who provides constructive feedback."},
            {"role": "user", "content": f"Please evaluate and provide feedback on the following candidate answer: {answer}"}
        ],
        "max_tokens": 200
    }
    
    response = requests.post(MISTRAL_API_URL, json=data, headers=headers, timeout=60)
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
