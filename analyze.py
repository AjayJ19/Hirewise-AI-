from textblob import TextBlob
import re

FILLER_WORDS = ["um", "uh", "like", "you know", "so", "basically", "I mean", "sort of"]

def analyze_sentiment(text):
    """
    Returns sentiment polarity and subjectivity.
    """
    blob = TextBlob(text)
    polarity = round(blob.sentiment.polarity, 2)  # [-1, 1]
    subjectivity = round(blob.sentiment.subjectivity, 2)  # [0, 1]
    return {
        "polarity": polarity,
        "subjectivity": subjectivity
    }

def detect_filler_words(text):
    """
    Counts filler words in the given response.
    """
    filler_count = sum(len(re.findall(rf'\b{re.escape(word)}\b', text.lower())) for word in FILLER_WORDS)
    return filler_count

def analyze_response(text):
    sentiment = analyze_sentiment(text)
    fillers = detect_filler_words(text)

    feedback = "Your response is "
    if sentiment["polarity"] > 0.3:
        feedback += "positive and confident. "
    elif sentiment["polarity"] < -0.2:
        feedback += "negative in tone. Try to be more optimistic. "
    else:
        feedback += "neutral. Add more enthusiasm. "

    if fillers > 3:
        feedback += f"Also, you used {fillers} filler words. Try to reduce them for a more professional impression."
    elif fillers > 0:
        feedback += f"You used a few filler words ({fillers}). Aim for smoother delivery."

    return {
        "sentiment": sentiment,
        "filler_words": fillers,
        "feedback": feedback
    }

# Optional webcam emotion analysis (Future)
# def analyze_face_webcam():
#     import cv2
#     import mediapipe as mp
#     mp_face_mesh = mp.solutions.face_mesh
#     cap = cv2.VideoCapture(0)
#     with mp_face_mesh.FaceMesh() as face_mesh:
#         while cap.isOpened():
#             ret, frame = cap.read()
#             if not ret:
#                 break
#             results = face_mesh.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
#             if results.multi_face_landmarks:
#                 print("Face Detected")
#             cv2.imshow("Webcam", frame)
#             if cv2.waitKey(1) & 0xFF == ord("q"):
#                 break
#     cap.release()
#     cv2.destroyAllWindows()
