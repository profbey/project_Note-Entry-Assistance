import tkinter as tk
from tkinter import ttk
from modules.data.student import Student, Grade
from datetime import datetime
import uuid

class StudentFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.setup_ui()
        
    def setup_ui(self):
        # Student List
        list_frame = ttk.LabelFrame(self, text="Students")
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.student_listbox = tk.Listbox(list_frame)
        self.student_listbox.pack(fill=tk.BOTH, expand=True)
        self.student_listbox.bind('<<ListboxSelect>>', self.on_select_student)
        
        # Student Details
        details_frame = ttk.LabelFrame(self, text="Student Details")
        details_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Add Student Form
        form_frame = ttk.Frame(details_frame)
        form_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(form_frame, text="First Name:").grid(row=0, column=0, padx=5, pady=5)
        self.first_name_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.first_name_var).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Last Name:").grid(row=1, column=0, padx=5, pady=5)
        self.last_name_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.last_name_var).grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Button(form_frame, text="Add Student", command=self.add_student).grid(row=2, column=0, columnspan=2, pady=10)
        
        # Grades Frame
        grades_frame = ttk.LabelFrame(details_frame, text="Grades")
        grades_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.grades_tree = ttk.Treeview(grades_frame, columns=("Date", "Grade", "Description"), show="headings")
        self.grades_tree.heading("Date", text="Date")
        self.grades_tree.heading("Grade", text="Grade")
        self.grades_tree.heading("Description", text="Description")
        self.grades_tree.pack(fill=tk.BOTH, expand=True)
        
    def update_content(self):
        self.student_listbox.delete(0, tk.END)
        students = self.controller.storage.load_students()
        for student in students:
            self.student_listbox.insert(tk.END, f"{student.first_name} {student.last_name}")
            
    def add_student(self):
        first_name = self.first_name_var.get().strip()
        last_name = self.last_name_var.get().strip()
        
        if first_name and last_name:
            students = self.controller.storage.load_students()
            new_student = Student(
                id=str(uuid.uuid4()),
                first_name=first_name,
                last_name=last_name,
                grades=[]
            )
            students.append(new_student)
            self.controller.storage.save_students(students)
            self.update_content()
            
            # Clear form
            self.first_name_var.set("")
            self.last_name_var.set("")
            
    def on_select_student(self, event):
        selection = self.student_listbox.curselection()
        if selection:
            students = self.controller.storage.load_students()
            student = students[selection[0]]
            
            # Update grades tree
            self.grades_tree.delete(*self.grades_tree.get_children())
            for grade in student.grades:
                self.grades_tree.insert("", tk.END, values=(
                    grade.date.strftime("%Y-%m-%d"),
                    grade.value if grade.value is not None else "N/A",
                    grade.description
                ))