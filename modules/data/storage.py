import json
import os
from typing import List, Dict
from datetime import datetime
from .student import Student, Grade

class Storage:
    def __init__(self):
        self.data_dir = "data"
        self.ensure_data_directory()
        
    def ensure_data_directory(self):
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            
    def save_students(self, students: List[Student]):
        data = []
        for student in students:
            student_dict = {
                "id": student.id,
                "first_name": student.first_name,
                "last_name": student.last_name,
                "grades": [
                    {
                        "value": grade.value,
                        "date": grade.date.isoformat(),
                        "description": grade.description
                    }
                    for grade in student.grades
                ]
            }
            data.append(student_dict)
            
        with open(os.path.join(self.data_dir, "students.json"), "w") as f:
            json.dump(data, f, indent=2)
            
    def load_students(self) -> List[Student]:
        try:
            with open(os.path.join(self.data_dir, "students.json"), "r") as f:
                data = json.load(f)
                
            students = []
            for student_dict in data:
                grades = [
                    Grade(
                        value=g["value"],
                        date=datetime.fromisoformat(g["date"]),
                        description=g["description"]
                    )
                    for g in student_dict["grades"]
                ]
                
                student = Student(
                    id=student_dict["id"],
                    first_name=student_dict["first_name"],
                    last_name=student_dict["last_name"],
                    grades=grades
                )
                students.append(student)
                
            return students
        except FileNotFoundError:
            return []