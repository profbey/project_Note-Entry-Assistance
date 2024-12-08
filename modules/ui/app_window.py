import tkinter as tk
from tkinter import ttk
from .student_frame import StudentFrame
from .analysis_frame import AnalysisFrame
from modules.data.storage import Storage

class AppWindow:
    def __init__(self, root):
        self.root = root
        self.storage = Storage()
        self.setup_ui()
        
    def setup_ui(self):
        # Configure grid
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=0)
        self.root.grid_rowconfigure(1, weight=1)
        
        # Create navigation
        self.create_navigation()
        
        # Create main content area
        self.content_frame = ttk.Frame(self.root)
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        
        # Initialize frames
        self.frames = {}
        for F in (StudentFrame, AnalysisFrame):
            frame = F(self.content_frame, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            
        self.show_frame(StudentFrame)
        
    def create_navigation(self):
        nav_frame = ttk.Frame(self.root)
        nav_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
        
        ttk.Button(
            nav_frame,
            text="Students",
            command=lambda: self.show_frame(StudentFrame)
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            nav_frame,
            text="Analysis",
            command=lambda: self.show_frame(AnalysisFrame)
        ).pack(side=tk.LEFT, padx=5)
        
    def show_frame(self, frame_class):
        frame = self.frames[frame_class]
        frame.tkraise()
        frame.update_content()