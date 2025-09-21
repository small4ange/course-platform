from datetime import date
from App.mixins import LoggingMixin, NotificationMixin
from App.interfaces import Teachable, Assessable
from typing import List, Dict, Any
from App.dto.course.Course import Course
from App.decorators import check_permissions
from App.exceptions import PermissionDeniedError

# -------- Курс по дизайну
class DesignCourse(Course, Teachable, Assessable, LoggingMixin, NotificationMixin):
    def __init__(self, title: str, start_date: date, end_date: date,
                 instructor: str, students: List[str], topics: List[str],
                 tools: List[str], current_user=None):
        super().__init__(title, start_date, end_date, instructor, students, topics)
        self.__tools = tools 
        self.current_user = current_user

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
    @check_permissions('instructor')
    def teach(self):
        self.log_action("Начало лекции по дизайну")
        self.notify_students("Началась лекция по дизайну")
        return "Объясняю принципы композиции"

    @check_permissions('instructor')
    def assess_progress(self, progress: Dict[str, float]):
        self.log_action("Оценка прогресса студентов")
        return self.calculate_completion_rate(progress)

    def to_dict(self) -> Dict[str, Any]:
        """Преобразует объект курса в словарь"""
        data = super().to_dict()
        data['tools'] = self.__tools
        if hasattr(self, 'current_user') and self.current_user:
            data['current_user'] = {
                'username': self.current_user.username,
                'role': self.current_user.role
            }
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DesignCourse':
        # Обрабатываем пользователя, если он есть в данных
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
            tools=data['tools'],
            current_user=current_user
        )