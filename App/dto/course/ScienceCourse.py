from datetime import date
from typing import List, Dict
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
        self.__field = field  # добавили поле для области науки

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
