from datetime import date
from typing import List, Dict, Any
from App.dto.course.Course import Course
from App.interfaces import Teachable, Assessable
from App.mixins import LoggingMixin, NotificationMixin
from App.decorators import check_permissions
from App.exceptions import PermissionDeniedError

# -------- Курс по науке
class ScienceCourse(Course, Teachable, Assessable, LoggingMixin, NotificationMixin):
    def __init__(self, title: str, start_date: date, end_date: date,
                 instructor: str, students: List[str], topics: List[str],
                 field: List[str], current_user=None):
        super().__init__(title, start_date, end_date, instructor, students, topics)
        self.__field = field  
        self.current_user = current_user

    # -------- геттер для field
    @property
    def field(self) -> List[str]:
        return self.__field

    # --------- переопределяем метод для расчета процента прохождения курса
    # аргументы: progress - словарь [студент, число выполненных заданий]
    def calculate_completion_rate(self, progress: Dict[str, float]) -> float:
        if not progress:
            return 0.0
        max_tasks = len(self.topics)
        avg = sum(min(v, max_tasks) / max_tasks for v in progress.values()) / len(progress)
        return avg * 100

    # -------- переопределяем метод вывода данных курса в строку
    def __str__(self) -> str:
        fields = ", ".join(self.__field)
        return f"Курс науки: {self.title}, Преподаватель: {self.instructor}, Области: {fields}"

    # --- Методы интерфейсов ---
    @check_permissions('instructor')
    def teach(self) -> str:
        self.log_action("Начало лабораторной работы")
        self.notify_students("Началась лабораторная работа")
        return "Провожу лабораторные работы"

    @check_permissions('instructor')
    def assess_progress(self, progress: Dict[str, float]) -> float:
        self.log_action("Оценка прогресса студентов")
        return self.calculate_completion_rate(progress)

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data['field'] = self.__field
        if hasattr(self, 'current_user') and self.current_user:
            data['current_user'] = {
                'username': self.current_user.username,
                'role': self.current_user.role
            }
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ScienceCourse':
        current_user = None
        if 'current_user' in data:
            from App.dto.User import User
            current_user = User(data['current_user']['username'], data['current_user']['role'])
        
        return cls(
            title=data['title'],
            start_date=data['start_date'],
            end_date=data['end_date'],
            instructor=data['instructor'],
            students=data['students'],
            topics=data['topics'],
            field=data['field'],
            current_user=current_user
        )