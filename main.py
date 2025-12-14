import time
from tts import speak
from stt import listen
from engine import generate_question, generate_feedback
from resume import parse_resume
from score import score_response

def main():
    print("🤖 AI Interview Bot Started")

    resume_path = "D:\\Workshop\\resume\\rr.pdf"
    resume_data = parse_resume("C:\Workshop-main\Workshop-main\Dev resume.pdf.pdf.pdf")

    speak("Welcome to your AI mock interview.")
    first_question = "Tell me about yourself."
    print(f"🤖 {first_question}")
    speak(first_question)

    all_answers = []

    user_input = listen()
    all_answers.append(user_input)

    for i in range(4):  # Ask 4 dynamic follow-ups
        print(f"\n🔁 Asking question {i + 1}")
        question = generate_question(user_input, resume_data)
        print(f"🤖 {question}")
        speak(question)

        user_input = listen()
        all_answers.append(user_input)

        if (i + 1) % 2 == 0:
            speak("Analyzing your last few answers...")
            feedback = generate_feedback(" ".join(all_answers[-2:]))
            print(f"🧠 Feedback: {feedback}")
            speak(feedback)

        time.sleep(1)

    speak("Thanks for attending the interview. Here is your final feedback.")
    final_feedback = generate_feedback(" ".join(all_answers))
    print(f"🏁 Final Feedback: {final_feedback}")
    speak(final_feedback)

    avg_score = sum(score_response(ans) for ans in all_answers) / len(all_answers)
    print(f"💯 Final Score: {round(avg_score, 2)}")
    speak(f"Your final score is {round(avg_score, 2)} out of 100")

if __name__ == "__main__":
    main()
