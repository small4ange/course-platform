from App.Course import Course
from datetime import date
from typing import List, Dict
from abc import ABC


# -------- Курс о науке
class ScienceCourse(Course):
    def __init__(self, title: str, start_date: date, end_date: date,
                 instructor: str, students: List[str], topics: List[str],
                 field: List[str]):
        super().__init__(title, start_date, end_date, instructor, students, topics)
        self.__field = field # добавили поле для области науки

    # -------- геттер для field
    @property
    def field(self) -> str:
        return self.__field

    # --------- переопределяем метод для расчета процента прохождения курса
    # аргументы: progress - словарь [студент, число выполненных заданий]
    def calculate_completion_rate(self, progress: Dict[str, float]) -> float:
        if not progress:
            return 0
        max_tasks = len(self.topics)
        avg = sum(min(v, max_tasks)/max_tasks for v in progress.values())/len(progress)
        return avg * 100

    # -------- переопределяем метод вывода данных курса в строку
    def __str__(self) -> str:
        tools = ", ".join(self.__tools)
        return f"Курс дизайна: {self.title}, Преподаватель: {self.instructor}, Инструменты: {tools}"
