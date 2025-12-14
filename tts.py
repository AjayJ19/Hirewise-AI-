import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 180)

def speak(text):
    try:
        print(f" Speaking: {text}")
        engine.say(text)
        engine.runAndWait()
    except RuntimeError:
        print(" TTS Error")
