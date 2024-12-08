import tkinter as tk
from tkinter import ttk
from modules.analysis.statistics import GradeAnalytics

class AnalysisFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.setup_ui()
        
    def setup_ui(self):
        # Statistics Section
        stats_frame = ttk.LabelFrame(self, text="Class Statistics")
        stats_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.stats_text = tk.Text(stats_frame, height=10, width=50)
        self.stats_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Grade Distribution Section
        dist_frame = ttk.LabelFrame(self, text="Grade Distribution")
        dist_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.dist_text = tk.Text(dist_frame, height=10, width=50)
        self.dist_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
    def update_content(self):
        students = self.controller.storage.load_students()
        stats = GradeAnalytics.calculate_class_statistics(students)
        
        # Update Statistics Text
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(tk.END, f"Class Average: {stats['mean']:.2f if stats['mean'] is not None else 'N/A'}\n")
        self.stats_text.insert(tk.END, f"Median Grade: {stats['median']:.2f if stats['median'] is not None else 'N/A'}\n")
        self.stats_text.insert(tk.END, f"Most Common Grade: {stats['mode']:.2f if stats['mode'] is not None else 'N/A'}\n")
        self.stats_text.insert(tk.END, f"Standard Deviation: {stats['std_dev']:.2f if stats['std_dev'] is not None else 'N/A'}\n")
        
        # Update Distribution Text
        self.dist_text.delete(1.0, tk.END)
        self.dist_text.insert(tk.END, "Grade Distribution:\n\n")
        for grade, count in stats['grade_distribution'].items():
            self.dist_text.insert(tk.END, f"{grade}: {count} students\n")