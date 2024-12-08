from typing import List, Dict
from modules.data.student import Student
import statistics
from collections import Counter

class GradeAnalytics:
    @staticmethod
    def calculate_class_statistics(students: List[Student]) -> Dict:
        grades = []
        for student in students:
            avg = student.calculate_average()
            if avg is not None:
                grades.append(avg)
                
        if not grades:
            return {
                "mean": None,
                "median": None,
                "mode": None,
                "std_dev": None,
                "grade_distribution": {}
            }
            
        letter_grades = [s.get_letter_grade() for s in students]
        grade_dist = Counter(letter_grades)
        
        return {
            "mean": statistics.mean(grades) if grades else None,
            "median": statistics.median(grades) if grades else None,
            "mode": statistics.mode(grades) if grades else None,
            "std_dev": statistics.stdev(grades) if len(grades) > 1 else None,
            "grade_distribution": dict(grade_dist)
        }