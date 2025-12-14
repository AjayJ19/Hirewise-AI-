# HireWise-AI
An intelligent voice-based mock interview assistant that helps you prepare for real-world interviews! 🚀  This Python-based application uses speech recognition, text-to-speech, resume parsing, and AI-generated questions and feedback to simulate a dynamic interview environment.
# 🎙️ AI Mock Interview Bot

## ✨ Features

- 📄 **Resume Parsing**  
  Upload a PDF resume and extract skills/experience using `PyMuPDF`.

- 🤖 **AI-Powered Interview Questions**  
  Dynamically generated based on your previous answers and resume using the **Mistral AI API**.

- 🎤 **Speech-to-Text (STT)**  
  Automatically listens and converts your spoken responses using `SpeechRecognition`.

- 🔊 **Text-to-Speech (TTS)**  
  Questions and feedback are read aloud using `pyttsx3`.

- 🧠 **Real-time Feedback**  
  Get constructive feedback after every few answers using Mistral.

- 📊 **Answer Scoring**  
  Uses `sentence-transformers` to semantically evaluate and score your responses.

- 🪟 **Graphical User Interface (GUI)**  
  Built with `Tkinter` for a simple and interactive experience.

---

## 🛠️ Tech Stack

| Component | Library/Tool |
|----------|---------------|
| GUI      | `Tkinter`     |
| Resume Parsing | `PyMuPDF` |
| STT      | `SpeechRecognition` |
| TTS      | `pyttsx3` or `gTTS` |
| AI Question/Feedback | `Mistral API` |
| Scoring  | `sentence-transformers` |

---

## 🚀 Getting Started

1. **Clone the repo**
   ```bash
   git clone https://github.com/your-username/ai-mock-interview-bot.git
   cd ai-mock-interview-bot
