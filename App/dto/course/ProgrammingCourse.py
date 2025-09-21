from App.dto.course.Course import Course
from datetime import date
from App.interfaces import Teachable, Assessable
from App.mixins import LoggingMixin, NotificationMixin
from typing import List, Dict, Any
from App.decorators import check_permissions
from App.exceptions import PermissionDeniedError

#-------- Курс по программированию
class ProgrammingCourse(Course, Teachable, Assessable, LoggingMixin, NotificationMixin):
    def __init__(self, title: str, start_date: date, end_date: date,
                 instructor: str, students: List[str], topics: List[str],
                 languages: List[str], current_user=None):
        super().__init__(title, start_date, end_date, instructor, students, topics)
        self.__languages = languages 
        self.current_user = current_user

    #-------- геттер для languaes
    @property
    def languages(self) -> List[str]:
        return self.__languages

    #--------- переопределяем метод для расчета процента прохождения курса
    # аргументы: progress - словарь [студент, доля пройденная в курсе от 0 до 1]
    def calculate_completion_rate(self, progress: Dict[str, float]) -> float:
        if not progress:
            return 0
        avg = sum(progress.values()) / len(progress)
        return avg * 100

    #-------- переопределяем метод вывода данных курса в строку
    def __str__(self) -> str:
        langs = ", ".join(self.__languages)
        return f"Курс программирования: {self.title}, Преподаватель: {self.instructor}, Языки: {langs}"

    # --- Методы интерфейса Teachable и Assessable ---
    @check_permissions('instructor')
    def teach(self):
        self.log_action("Начало лекции")  # логирование
        self.notify_students("Началась лекция по алгоритмам")  # уведомление
        return "Провожу лекции по алгоритмам"

    @check_permissions('instructor')
    def assess_progress(self, progress: Dict[str, float]):
        self.log_action("Оценка прогресса студентов")
        return self.calculate_completion_rate(progress)

    def to_dict(self) -> Dict[str, Any]:
        """Преобразует объект курса в словарь"""
        data = super().to_dict()
        data['languages'] = self.__languages
        if hasattr(self, 'current_user') and self.current_user:
            data['current_user'] = {
                'username': self.current_user.username,
                'role': self.current_user.role
            }
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ProgrammingCourse':
        """Создает объект курса из словаря"""
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
            languages=data['languages'],
            current_user=current_user
        )