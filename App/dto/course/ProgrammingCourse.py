from App.dto.course.Course import Course
from datetime import date
from App.interfaces import Teachable, Assessable
from App.mixins import LoggingMixin, NotificationMixin
from typing import List, Dict
from App.dto.ProgressAssessors import ProgrammingProgressAssessor


#-------- Курс по программированию
class ProgrammingCourse(Course, Teachable, Assessable, LoggingMixin, NotificationMixin):
    def __init__(self, title: str, start_date: date, end_date: date,
                 instructor: str, students: List[str], topics: List[str],
                 languages: List[str]):
        super().__init__(title, start_date, end_date, instructor, students, topics)
        self.__languages = languages # добавили поле languages

    #-------- геттер для languaes
    @property
    def languages(self) -> List[str]:
        return self.__languages

    #  Метод для оценки прогресса
    def create_progress_assessor(self):
        return ProgrammingProgressAssessor(self)  # Передаем self как курс

    #-------- переопределяем метод вывода данных курса в строку
    def __str__(self) -> str:
        langs = ", ".join(self.__languages)
        return f"Курс программирования: {self.title}, Преподаватель: {self.instructor}, Языки: {langs}"

        # --- Методы интерфейса Teachable и Assessable ---
    def teach(self):
            self.log_action("Начало лекции")  # логирование
            self.notify_students("Началась лекция по алгоритмам")  # уведомление
            return "Провожу лекции по алгоритмам"

    def assess_progress(self, progress: Dict[str, float]):
            self.log_action("Оценка прогресса студентов")
            return super().assess_progress(progress)