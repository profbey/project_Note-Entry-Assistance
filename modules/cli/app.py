import os
from datetime import datetime
import uuid
from modules.data.storage import Storage
from modules.data.student import Student, Grade
from modules.analysis.statistics import GradeAnalytics

class TeacherAssistantCLI:
    def __init__(self):
        self.storage = Storage()
        self.commands = {
            '1': ('Add Student', self.add_student),
            '2': ('List Students', self.list_students),
            '3': ('Add Grade', self.add_grade),
            '4': ('View Student Details', self.view_student),
            '5': ('View Class Statistics', self.view_statistics),
            '6': ('Exit', lambda: True)
        }

    def clear_screen(self):
        os.system('clear' if os.name != 'nt' else 'cls')

    def print_menu(self):
        self.clear_screen()
        print("\n=== Teacher's Assistant ===\n")
        for key, (label, _) in self.commands.items():
            print(f"{key}. {label}")
        print()

    def get_input(self, prompt, validator=None):
        while True:
            value = input(prompt).strip()
            if validator is None or validator(value):
                return value
            print("Invalid input. Please try again.")

    def add_student(self):
        print("\n=== Add New Student ===\n")
        first_name = self.get_input("Enter first name: ", lambda x: len(x) > 0)
        last_name = self.get_input("Enter last name: ", lambda x: len(x) > 0)

        students = self.storage.load_students()
        new_student = Student(
            id=str(uuid.uuid4()),
            first_name=first_name,
            last_name=last_name,
            grades=[]
        )
        students.append(new_student)
        self.storage.save_students(students)
        print("\nStudent added successfully!")
        input("\nPress Enter to continue...")

    def list_students(self):
        print("\n=== Student List ===\n")
        students = self.storage.load_students()
        if not students:
            print("No students found.")
        else:
            for i, student in enumerate(students, 1):
                print(f"{i}. {student.first_name} {student.last_name}")
        input("\nPress Enter to continue...")

    def add_grade(self):
        students = self.storage.load_students()
        if not students:
            print("\nNo students found. Please add a student first.")
            input("\nPress Enter to continue...")
            return

        print("\n=== Add Grade ===\n")
        print("Select a student:")
        for i, student in enumerate(students, 1):
            print(f"{i}. {student.first_name} {student.last_name}")

        def validate_student(x):
            try:
                return 1 <= int(x) <= len(students)
            except ValueError:
                return False

        student_idx = int(self.get_input("\nEnter student number: ", validate_student)) - 1
        student = students[student_idx]

        def validate_grade(x):
            try:
                return 0 <= float(x) <= 100
            except ValueError:
                return False

        grade_value = float(self.get_input("Enter grade (0-100): ", validate_grade))
        description = self.get_input("Enter description: ", lambda x: len(x) > 0)

        grade = Grade(
            value=grade_value,
            date=datetime.now(),
            description=description
        )
        student.grades.append(grade)
        self.storage.save_students(students)
        print("\nGrade added successfully!")
        input("\nPress Enter to continue...")

    def view_student(self):
        students = self.storage.load_students()
        if not students:
            print("\nNo students found.")
            input("\nPress Enter to continue...")
            return

        print("\n=== View Student Details ===\n")
        print("Select a student:")
        for i, student in enumerate(students, 1):
            print(f"{i}. {student.first_name} {student.last_name}")

        def validate_student(x):
            try:
                return 1 <= int(x) <= len(students)
            except ValueError:
                return False

        student_idx = int(self.get_input("\nEnter student number: ", validate_student)) - 1
        student = students[student_idx]

        print(f"\nStudent: {student.first_name} {student.last_name}")
        print(f"Average Grade: {student.calculate_average():.2f if student.calculate_average() is not None else 'N/A'}")
        print(f"Letter Grade: {student.get_letter_grade()}")
        print("\nGrades:")
        if not student.grades:
            print("No grades recorded")
        else:
            for grade in student.grades:
                print(f"Date: {grade.date.strftime('%Y-%m-%d')}, Grade: {grade.value}, Description: {grade.description}")
        input("\nPress Enter to continue...")

    def view_statistics(self):
        print("\n=== Class Statistics ===\n")
        students = self.storage.load_students()
        if not students:
            print("No students found.")
            input("\nPress Enter to continue...")
            return

        stats = GradeAnalytics.calculate_class_statistics(students)
        print(f"Class Average: {stats['mean']:.2f if stats['mean'] is not None else 'N/A'}")
        print(f"Median Grade: {stats['median']:.2f if stats['median'] is not None else 'N/A'}")
        print(f"Most Common Grade: {stats['mode']:.2f if stats['mode'] is not None else 'N/A'}")
        print(f"Standard Deviation: {stats['std_dev']:.2f if stats['std_dev'] is not None else 'N/A'}")
        
        print("\nGrade Distribution:")
        for grade, count in stats['grade_distribution'].items():
            print(f"{grade}: {count} students")
        input("\nPress Enter to continue...")

    def run(self):
        while True:
            self.print_menu()
            choice = self.get_input("Enter your choice: ", lambda x: x in self.commands)
            if self.commands[choice][1]():
                break