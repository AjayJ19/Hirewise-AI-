#!/usr/bin/env python3
"""
HireWise AI Interview Bot - Enhanced UI Launcher
===============================================

This script launches the modern, enhanced UI for the AI Interview Bot.
"""

import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import tkinter as tk
    from ui import ModernInterviewApp
    
    def main():
        """Launch the enhanced interview application"""
        print("🚀 Starting HireWise AI Interview Bot...")
        print("📱 Loading enhanced user interface...")
        
        # Create the main window
        root = tk.Tk()
        
        # Set window icon (if available)
        try:
            root.iconbitmap('icon.ico')  # You can add an icon file later
        except:
            pass
        
        # Create and run the application
        app = ModernInterviewApp(root)
        
        print("✅ Application loaded successfully!")
        print("💡 Tips:")
        print("   - Upload your resume first")
        print("   - Click 'Start Interview' to begin")
        print("   - Speak clearly when answering questions")
        print("   - Use 'Stop Interview' if you need to pause")
        
        # Start the main event loop
        root.mainloop()
        
    if __name__ == "__main__":
        main()
        
except ImportError as e:
    print(f"❌ Error: Missing required module - {e}")
    print("💡 Please install required dependencies:")
    print("   pip install -r req.txt")
    
except Exception as e:
    print(f"❌ Error starting application: {e}")
    print("💡 Please check that all files are present and dependencies are installed.") 