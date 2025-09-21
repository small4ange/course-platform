from datetime import date
from typing import List, Dict, Any
from App.dto.course.Course import Course
from App.interfaces import Teachable, Assessable
from App.mixins import LoggingMixin, NotificationMixin
from App.dto.ProgressAssessors import ScienceProgressAssessor

# -------- Курс по науке
class ScienceCourse(Course, Teachable, Assessable, LoggingMixin, NotificationMixin):
    def __init__(self, title: str, start_date: date, end_date: date,
                 instructor: str, students: List[str], topics: List[str],
                 field: List[str]):
        super().__init__(title, start_date, end_date, instructor, students, topics)
        self.__field = field

    # -------- геттер для field
    @property
    def field(self) -> List[str]:
        return self.__field

    #  Метод для оценки прогресса
    def create_progress_assessor(self):
        return ScienceProgressAssessor(self)  # Передаем self как курс

    # -------- переопределяем метод вывода данных курса в строку
    def __str__(self) -> str:
        fields = ", ".join(self.__field)
        return f"Курс науки: {self.title}, Преподаватель: {self.instructor}, Области: {fields}"

    # --- Методы интерфейсов ---
    def teach(self) -> str:
        self.log_action("Начало лабораторной работы")
        self.notify_students("Началась лабораторная работа")
        return "Провожу лабораторные работы"

    def assess_progress(self, progress: Dict[str, float]) -> float:
        self.log_action("Оценка прогресса студентов")
        return super().assess_progress(progress)
    
    
    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data.update({
            'field': self.__field
        })
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ScienceCourse':
        start_date = date.fromisoformat(data['start_date'])
        end_date = date.fromisoformat(data['end_date'])
        
        course = cls(
            title=data['title'],
            start_date=start_date,
            end_date=end_date,
            instructor=data['instructor'],
            students=data['students'],
            topics=data['topics'],
            field=data.get('field', [])
        )
        
        return course