from datetime import date
from App.mixins import LoggingMixin, NotificationMixin
from App.interfaces import Teachable, Assessable
from typing import List, Dict, Any
from App.dto.course.Course import Course
from App.dto.ProgressAssessors import DesignProgressAssessor

# -------- Курс по дизайну
class DesignCourse(Course, Teachable, Assessable, LoggingMixin, NotificationMixin):
    def __init__(self, title: str, start_date: date, end_date: date,
                 instructor: str, students: List[str], topics: List[str],
                 tools: List[str]):
        super().__init__(title, start_date, end_date, instructor, students, topics)
        self.__tools = tools

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
    
    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data.update({
            'tools': self.__tools
        })
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DesignCourse':
        start_date = date.fromisoformat(data['start_date'])
        end_date = date.fromisoformat(data['end_date'])
        
        course = cls(
            title=data['title'],
            start_date=start_date,
            end_date=end_date,
            instructor=data['instructor'],
            students=data['students'],
            topics=data['topics'],
            tools=data.get('tools', [])
        )
        
        return course