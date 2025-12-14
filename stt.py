import speech_recognition as sr

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening... (Start speaking)")
        r.pause_threshold = 1.0  # Wait until user stops speaking
        r.energy_threshold = 300  # Optional: adjust for your mic
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        print(f"🗣️ You said: {text}")
        return text
    except sr.UnknownValueError:
        print("❌ Could not understand audio.")
        return input("❗ STT failed. Type your response instead: ")
    except sr.RequestError:
        print("❌ STT service failed.")
        return input("❗ STT failed. Type your response instead: ")
