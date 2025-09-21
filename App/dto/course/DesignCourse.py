from datetime import date
from App.mixins import LoggingMixin, NotificationMixin
from App.interfaces import Teachable, Assessable
from typing import List, Dict
from App.dto.course.Course import Course
from App.dto.ProgressAssessors import DesignProgressAssessor

# -------- Курс по дизайну
class DesignCourse(Course, Teachable, Assessable, LoggingMixin, NotificationMixin):
    def __init__(self, title: str, start_date: date, end_date: date,
                 instructor: str, students: List[str], topics: List[str],
                 tools: List[str]):
        super().__init__(title, start_date, end_date, instructor, students, topics)
        self.__tools = tools # добавили поле с изучаемыми инструментами

    # -------- геттер для tools
    @property
    def tools(self) -> List[str]:
        return self.__tools

    #  Метод для оценки прогресса
    def create_progress_assessor(self):
        return DesignProgressAssessor(self)  # Передаем self как курс

    # -------- переопределяем метод вывода данных курса в строку
    def __str__(self) -> str:
        tools = ", ".join(self.__tools)
        return f"Курс дизайна: {self.title}, Преподаватель: {self.instructor}, Инструменты: {tools}"

        # --- Методы интерфейса ---
    def teach(self):
            self.log_action("Начало лекции по дизайну")
            self.notify_students("Началась лекция по дизайну")
            return "Объясняю принципы композиции"

    def assess_progress(self, progress: Dict[str, float]):
            self.log_action("Оценка прогресса студентов")
            return super().assess_progress(progress)