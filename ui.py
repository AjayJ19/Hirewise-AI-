import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import os
import threading
from tts import speak
from stt import listen
from engine import generate_question, generate_feedback
from resume import parse_resume
from score import score_response
from datetime import datetime

class ModernInterviewApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎯 HireWise AI - Smart Interview Assistant")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f8f9fa")
        self.root.minsize(900, 600)

        # Variables
        self.chat_log = []
        self.resume_data = None
        self.interview_running = False
        self.current_question_count = 0
        self.total_questions = 5

        # Configure styles
        self.setup_styles()
        
        # Create main container
        self.main_frame = tk.Frame(root, bg="#f8f9fa")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Create header
        self.create_header()
        
        # Create main content area
        self.create_content_area()
        
        # Create status bar
        self.create_status_bar()

    def setup_styles(self):
        """Configure custom styles for the application"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure button styles
        style.configure('Primary.TButton', 
                       background='#007bff', 
                       foreground='white',
                       font=('Segoe UI', 10, 'bold'),
                       padding=(20, 10))
        
        style.configure('Success.TButton',
                       background='#28a745',
                       foreground='white',
                       font=('Segoe UI', 10, 'bold'),
                       padding=(20, 10))
        
        style.configure('Warning.TButton',
                       background='#ffc107',
                       foreground='#212529',
                       font=('Segoe UI', 10, 'bold'),
                       padding=(20, 10))

    def create_header(self):
        """Create the application header"""
        header_frame = tk.Frame(self.main_frame, bg="#ffffff", relief="flat", bd=1)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Logo and title
        title_frame = tk.Frame(header_frame, bg="#ffffff")
        title_frame.pack(fill=tk.X, padx=20, pady=15)
        
        # Main title
        title_label = tk.Label(title_frame, 
                              text="🎯 HireWise AI", 
                              font=("Segoe UI", 24, "bold"), 
                              bg="#ffffff", 
                              fg="#2c3e50")
        title_label.pack(side=tk.LEFT)
        
        # Subtitle
        subtitle_label = tk.Label(title_frame, 
                                 text="Smart Interview Assistant", 
                                 font=("Segoe UI", 12), 
                                 bg="#ffffff", 
                                 fg="#6c757d")
        subtitle_label.pack(side=tk.LEFT, padx=(10, 0), pady=(5, 0))

    def create_content_area(self):
        """Create the main content area with sidebar and chat"""
        content_frame = tk.Frame(self.main_frame, bg="#ffffff", relief="flat", bd=1)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create sidebar
        self.create_sidebar(content_frame)
        
        # Create chat area
        self.create_chat_area(content_frame)

    def create_sidebar(self, parent):
        """Create the sidebar with controls"""
        sidebar_frame = tk.Frame(parent, bg="#f8f9fa", width=300, relief="flat", bd=1)
        sidebar_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 1))
        sidebar_frame.pack_propagate(False)
        
        # Resume section
        resume_frame = tk.Frame(sidebar_frame, bg="#ffffff", relief="flat", bd=1)
        resume_frame.pack(fill=tk.X, padx=10, pady=10)
        
        resume_title = tk.Label(resume_frame, 
                               text="📄 Resume Upload", 
                               font=("Segoe UI", 14, "bold"), 
                               bg="#ffffff", 
                               fg="#2c3e50")
        resume_title.pack(pady=(15, 10))
        
        self.upload_btn = ttk.Button(resume_frame, 
                                    text="Choose Resume File", 
                                    command=self.upload_resume,
                                    style='Primary.TButton')
        self.upload_btn.pack(pady=(0, 15))
        
        # Resume status
        self.resume_status = tk.Label(resume_frame, 
                                     text="No resume uploaded", 
                                     font=("Segoe UI", 10), 
                                     bg="#ffffff", 
                                     fg="#6c757d")
        self.resume_status.pack(pady=(0, 15))
        
        # Interview controls
        interview_frame = tk.Frame(sidebar_frame, bg="#ffffff", relief="flat", bd=1)
        interview_frame.pack(fill=tk.X, padx=10, pady=10)
        
        interview_title = tk.Label(interview_frame, 
                                  text="🎤 Interview Controls", 
                                  font=("Segoe UI", 14, "bold"), 
                                  bg="#ffffff", 
                                  fg="#2c3e50")
        interview_title.pack(pady=(15, 10))
        
        self.start_btn = ttk.Button(interview_frame, 
                                   text="🚀 Start Interview", 
                                   command=self.start_interview_thread,
                                   style='Success.TButton')
        self.start_btn.pack(pady=(0, 10))
        
        self.stop_btn = ttk.Button(interview_frame, 
                                  text="⏹️ Stop Interview", 
                                  command=self.stop_interview,
                                  style='Warning.TButton',
                                  state='disabled')
        self.stop_btn.pack(pady=(0, 15))
        
        # Progress section
        progress_frame = tk.Frame(sidebar_frame, bg="#ffffff", relief="flat", bd=1)
        progress_frame.pack(fill=tk.X, padx=10, pady=10)
        
        progress_title = tk.Label(progress_frame, 
                                 text="📊 Progress", 
                                 font=("Segoe UI", 14, "bold"), 
                                 bg="#ffffff", 
                                 fg="#2c3e50")
        progress_title.pack(pady=(15, 10))
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, 
                                           variable=self.progress_var,
                                           maximum=self.total_questions,
                                           length=200)
        self.progress_bar.pack(pady=(0, 10))
        
        # Progress text
        self.progress_text = tk.Label(progress_frame, 
                                     text="0 / 5 questions completed", 
                                     font=("Segoe UI", 10), 
                                     bg="#ffffff", 
                                     fg="#6c757d")
        self.progress_text.pack(pady=(0, 15))

    def create_chat_area(self, parent):
        """Create the chat display area"""
        chat_frame = tk.Frame(parent, bg="#ffffff")
        chat_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(1, 0))
        
        # Chat header
        chat_header = tk.Frame(chat_frame, bg="#e9ecef", height=50)
        chat_header.pack(fill=tk.X)
        chat_header.pack_propagate(False)
        
        chat_title = tk.Label(chat_header, 
                             text="💬 Interview Conversation", 
                             font=("Segoe UI", 14, "bold"), 
                             bg="#e9ecef", 
                             fg="#495057")
        chat_title.pack(side=tk.LEFT, padx=15, pady=15)
        
        # Clear chat button
        clear_btn = ttk.Button(chat_header, 
                              text="🗑️ Clear", 
                              command=self.clear_chat,
                              style='Warning.TButton')
        clear_btn.pack(side=tk.RIGHT, padx=15, pady=10)
        
        # Chat display
        self.text_area = scrolledtext.ScrolledText(
            chat_frame, 
            wrap=tk.WORD, 
            font=("Segoe UI", 11),
            bg="#ffffff", 
            fg="#212529", 
            insertbackground="#007bff",
            relief="flat",
            padx=15,
            pady=15
        )
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        self.text_area.configure(state='disabled')

    def create_status_bar(self):
        """Create the status bar"""
        status_frame = tk.Frame(self.main_frame, bg="#e9ecef", height=30)
        status_frame.pack(fill=tk.X, pady=(10, 0))
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(status_frame, 
                                    text="Ready to start interview", 
                                    font=("Segoe UI", 9), 
                                    bg="#e9ecef", 
                                    fg="#6c757d")
        self.status_label.pack(side=tk.LEFT, padx=15, pady=8)
        
        # Current time
        self.time_label = tk.Label(status_frame, 
                                  text="", 
                                  font=("Segoe UI", 9), 
                                  bg="#e9ecef", 
                                  fg="#6c757d")
        self.time_label.pack(side=tk.RIGHT, padx=15, pady=8)
        self.update_time()

    def update_time(self):
        """Update the time display"""
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.config(text=f"🕐 {current_time}")
        self.root.after(1000, self.update_time)

    def upload_resume(self):
        """Handle resume upload"""
        file_path = filedialog.askopenfilename(
            title="Select Resume",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if file_path:
            try:
                self.resume_data = parse_resume(file_path)
                filename = os.path.basename(file_path)
                self.resume_status.config(
                    text=f"✅ {filename}",
                    fg="#28a745"
                )
                self.status_label.config(text="Resume uploaded successfully")
                messagebox.showinfo("Success", f"✅ Resume '{filename}' uploaded successfully!")
            except Exception as e:
                self.resume_status.config(text="❌ Upload failed", fg="#dc3545")
                self.status_label.config(text="Failed to upload resume")
                messagebox.showerror("Error", f"Failed to parse resume.\n{str(e)}")

    def start_interview_thread(self):
        """Start interview in a separate thread"""
        if not self.resume_data:
            messagebox.showwarning("No Resume", "Please upload a resume before starting the interview.")
            return
        
        if self.interview_running:
            return
            
        self.interview_running = True
        self.start_btn.config(state='disabled')
        self.stop_btn.config(state='normal')
        self.upload_btn.config(state='disabled')
        
        thread = threading.Thread(target=self.run_interview)
        thread.daemon = True
        thread.start()

    def stop_interview(self):
        """Stop the current interview"""
        self.interview_running = False
        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
        self.upload_btn.config(state='normal')
        self.status_label.config(text="Interview stopped")
        self.add_message("System", "Interview stopped by user.", "system")

    def run_interview(self):
        """Run the interview process"""
        if not self.interview_running:
            return
            
        self.clear_chat()
        self.current_question_count = 0
        self.update_progress()
        
        self.add_message("AI", "Welcome to your AI mock interview! I'll be asking you questions based on your resume and your responses. Let's begin!", "ai")
        self.status_label.config(text="Starting interview...")
        speak("Welcome to your AI mock interview.")

        first_question = "Tell me about yourself."
        self.ask_question(first_question)

        all_answers = []
        user_input = listen()
        if not self.interview_running:
            return
        self.add_message("You", user_input, "user")
        all_answers.append(user_input)

        for i in range(4):
            if not self.interview_running:
                return
                
            question = generate_question(user_input, self.resume_data)
            self.ask_question(question)

            user_input = listen()
            if not self.interview_running:
                return
            self.add_message("You", user_input, "user")
            all_answers.append(user_input)

            if (i + 1) % 2 == 0:
                self.add_message("AI", "Analyzing your last few answers...", "ai")
                speak("Analyzing your last few answers...")
                feedback = generate_feedback(" ".join(all_answers[-2:]))
                self.add_message("AI", f"🧠 Feedback: {feedback}", "feedback")
                speak(feedback)

        if not self.interview_running:
            return
            
        self.add_message("AI", "Thanks for attending the interview. Here is your final feedback.", "ai")
        speak("Thanks for attending the interview. Here is your final feedback.")
        
        final_feedback = generate_feedback(" ".join(all_answers))
        self.add_message("AI", f"🏁 Final Feedback: {final_feedback}", "feedback")
        speak(final_feedback)

        avg_score = sum(score_response(ans) for ans in all_answers) / len(all_answers)
        score_text = f"💯 Final Score: {round(avg_score, 2)} / 100"
        self.add_message("AI", score_text, "score")
        speak(score_text)
        
        self.interview_running = False
        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
        self.upload_btn.config(state='normal')
        self.status_label.config(text="Interview completed")

    def ask_question(self, question):
        """Ask a question and update progress"""
        self.add_message("AI", question, "ai")
        speak(question)
        self.current_question_count += 1
        self.update_progress()

    def update_progress(self):
        """Update the progress bar and text"""
        progress = min(self.current_question_count, self.total_questions)
        self.progress_var.set(progress)
        self.progress_text.config(text=f"{progress} / {self.total_questions} questions completed")

    def add_message(self, sender, message, msg_type="normal"):
        """Add a message to the chat with styling"""
        self.text_area.configure(state='normal')
        
        # Add timestamp
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Style based on message type
        if msg_type == "ai":
            prefix = "🤖 AI"
            color = "#007bff"
        elif msg_type == "user":
            prefix = "👤 You"
            color = "#28a745"
        elif msg_type == "feedback":
            prefix = "🧠 AI"
            color = "#ffc107"
        elif msg_type == "score":
            prefix = "💯 AI"
            color = "#dc3545"
        elif msg_type == "system":
            prefix = "⚙️ System"
            color = "#6c757d"
        else:
            prefix = sender
            color = "#6c757d"
        
        # Insert message with styling
        self.text_area.insert(tk.END, f"[{timestamp}] {prefix}: {message}\n\n")
        
        # Apply color to the last message
        last_line_start = self.text_area.index("end-3l linestart")
        last_line_end = self.text_area.index("end-1c")
        
        # Create tag for this message
        tag_name = f"msg_{timestamp.replace(':', '_')}"
        self.text_area.tag_add(tag_name, last_line_start, last_line_end)
        self.text_area.tag_config(tag_name, foreground=color)
        
        self.text_area.see(tk.END)
        self.text_area.configure(state='disabled')

    def clear_chat(self):
        """Clear the chat area"""
        self.text_area.configure(state='normal')
        self.text_area.delete('1.0', tk.END)
        self.text_area.configure(state='disabled')
        self.current_question_count = 0
        self.update_progress()

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernInterviewApp(root)
    root.mainloop()


   