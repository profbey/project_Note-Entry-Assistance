from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class Grade:
    value: Optional[float]
    date: datetime
    description: str

@dataclass
class Student:
    id: str
    first_name: str
    last_name: str
    grades: List[Grade]
    
    def calculate_average(self) -> Optional[float]:
        valid_grades = [g.value for g in self.grades if g.value is not None]
        if not valid_grades:
            return None
        return sum(valid_grades) / len(valid_grades)
    
    def get_letter_grade(self) -> str:
        avg = self.calculate_average()
        if avg is None:
            return "N/A"
        
        if avg >= 90:
            return "A"
        elif avg >= 80:
            return "B"
        elif avg >= 70:
            return "C"
        elif avg >= 60:
            return "D"
        else:
            return "F"