from datetime import date
from App.mixins import LoggingMixin, NotificationMixin
from App.interfaces import Teachable, Assessable
from typing import List, Dict
from App.dto.course.Course import Course


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

    # --------- переопределяем метод для расчета процента прохождения курса
    # аргументы: progress - словарь [студент, оценка за сданную итоговую курсовую от 0 до 100]
    def calculate_completion_rate(self, progress: Dict[str, float]) -> float:
        if not progress:
            return 0
        avg = sum(progress.values()) / len(progress)
        return avg

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
            return self.calculate_completion_rate(progress)