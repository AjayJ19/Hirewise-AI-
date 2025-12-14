import streamlit as st
import os
from gtts import gTTS
import speech_recognition as sr
from streamlit_mic_recorder import mic_recorder
import tempfile
from engine import generate_question, generate_feedback
from resume import parse_resume
from score import score_response
import base64

# Page config
st.set_page_config(page_title="HireWise AI", page_icon="🎯", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    .chat-message {
        padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
    }
    .chat-message.user {
        background-color: #2b313e
    }
    .chat-message.bot {
        background-color: #475063
    }
    .chat-message .avatar {
      width: 20%;
    }
    .chat-message .message {
      width: 80%;
    }
    </style>
""", unsafe_allow_html=True)

def text_to_speech(text):
    """Generate audio from text and return the audio bytes"""
    try:
        tts = gTTS(text=text, lang='en')
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts.save(fp.name)
            with open(fp.name, "rb") as f:
                audio_bytes = f.read()
            os.unlink(fp.name)
            return audio_bytes
    except Exception as e:
        st.error(f"TTS Error: {e}")
        return None

def speech_to_text(audio_bytes):
    """Convert audio bytes to text"""
    r = sr.Recognizer()
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as fp:
            fp.write(audio_bytes)
            fp.close()
            
            with sr.AudioFile(fp.name) as source:
                audio_data = r.record(source)
                text = r.recognize_google(audio_data)
                os.unlink(fp.name)
                return text
    except Exception as e:
        st.error(f"STT Error: {e}")
        return None

def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
    if "question_count" not in st.session_state:
        st.session_state.question_count = 0
    if "interview_active" not in st.session_state:
        st.session_state.interview_active = False
    if "resume_data" not in st.session_state:
        st.session_state.resume_data = None
    if "answers" not in st.session_state:
        st.session_state.answers = []

initialize_session_state()

# Sidebar
with st.sidebar:
    st.title("🎯 HireWise AI")
    st.write("Smart Interview Assistant")
    
    # API Key Handling
    api_key = st.text_input("Mistral API Key", type="password", help="Enter your Mistral API Key here if not set in secrets.")
    
    # Try to load from secrets if not provided
    if not api_key:
        try:
            api_key = st.secrets["MISTRAL_API_KEY"]
            st.success("API Key loaded from Secrets ✅")
        except:
            st.warning("⚠️ No API Key found in Secrets.")
            
    # Simulation Mode
    simulated_mode = st.checkbox("Simulated Mode (No API required)", value=False, help="Check this to test the UI without an API key.")

    uploaded_file = st.file_uploader("Upload Resume (PDF)", type="pdf")
    
    if uploaded_file is not None:
        if st.session_state.resume_data is None:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_path = tmp_file.name
            
            try:
                st.session_state.resume_data = parse_resume(tmp_path)
                st.success("Resume uploaded successfully!")
                os.unlink(tmp_path)
            except Exception as e:
                st.error(f"Error parsing resume: {e}")

    if st.session_state.resume_data and not st.session_state.interview_active:
        if st.button("Start Interview", type="primary"):
            if not api_key and not simulated_mode:
                st.error("Please enter an API Key or enable Simulated Mode.")
            else:
                st.session_state.interview_active = True
                st.session_state.question_count = 0
                st.session_state.answers = []
                st.session_state.messages = []
                
                # First question
                first_q = "Tell me about yourself."
                st.session_state.current_question = first_q
                st.session_state.messages.append({"role": "assistant", "content": first_q})
                st.rerun()

    if st.session_state.interview_active:
        st.progress(st.session_state.question_count / 5, text=f"Question {st.session_state.question_count + 1}/5")
        if st.button("End Interview"):
            st.session_state.interview_active = False
            st.rerun()

# Main Chat Area
st.title("Interview Session")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
        if message.get("audio"):
            st.audio(message["audio"], format="audio/mp3")

# Interview Logic
if st.session_state.interview_active and st.session_state.question_count < 5:
    
    # Audio Input
    st.write("### Your Answer")
    audio_input = mic_recorder(
        start_prompt="🎤 Start Recording",
        stop_prompt="⏹️ Stop Recording",
        key='recorder',
        format='wav'
    )
    
    # Text Input Fallback
    text_input = st.chat_input("Or type your answer here...")

    user_answer = None
    
    if audio_input:
        with st.spinner("Processing audio..."):
            user_answer = speech_to_text(audio_input['bytes'])
    elif text_input:
        user_answer = text_input

    if user_answer:
        # Add user answer to chat
        st.session_state.messages.append({"role": "user", "content": user_answer})
        st.session_state.answers.append(user_answer)
        
        # Process answer and generate next step
        with st.spinner("Analyzing answer..."):
            
            # Generate feedback every 2 questions
            if (st.session_state.question_count + 1) % 2 == 0:
                if simulated_mode:
                    feedback = "This is a simulated feedback message. Your answer was recorded."
                else:
                    feedback = generate_feedback(" ".join(st.session_state.answers[-2:]), api_key)
                
                st.session_state.messages.append({"role": "assistant", "content": f"🧠 **Feedback:** {feedback}"})

            st.session_state.question_count += 1
            
            if st.session_state.question_count < 5:
                # Generate next question
                if simulated_mode:
                    next_q = f"This is simulated question #{st.session_state.question_count + 1}. Tell me more about your experience."
                else:
                    next_q = generate_question(user_answer, st.session_state.resume_data, api_key)
                
                st.session_state.current_question = next_q
                
                # Generate audio for question
                audio_bytes = text_to_speech(next_q)
                
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": next_q,
                    "audio": audio_bytes
                })
            else:
                # Final Feedback
                if simulated_mode:
                    final_feedback = "This is simulated final feedback. Good job!"
                else:
                    final_feedback = generate_feedback(" ".join(st.session_state.answers), api_key)
                
                st.session_state.messages.append({"role": "assistant", "content": f"🏁 **Final Feedback:** {final_feedback}"})
                
                # Score
                avg_score = sum(score_response(ans) for ans in st.session_state.answers) / len(st.session_state.answers)
                st.session_state.messages.append({"role": "assistant", "content": f"💯 **Final Score:** {round(avg_score, 2)}/100"})
                
                st.session_state.interview_active = False
        
        st.rerun()

elif not st.session_state.interview_active and st.session_state.question_count >= 5:
    st.success("Interview Completed! 🎉")
    if st.button("Start New Interview"):
        st.session_state.clear()
        st.rerun()
