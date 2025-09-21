from App.dto.course.Course import Course
from datetime import date
from App.interfaces import Teachable, Assessable
from App.mixins import LoggingMixin, NotificationMixin
from typing import List, Dict, Any
from App.dto.ProgressAssessors import ProgrammingProgressAssessor


#-------- Курс по программированию
class ProgrammingCourse(Course, Teachable, Assessable, LoggingMixin, NotificationMixin):
    def __init__(self, title: str, start_date: date, end_date: date,
                 instructor: str, students: List[str], topics: List[str],
                 languages: List[str]):
        super().__init__(title, start_date, end_date, instructor, students, topics)
        self.__languages = languages

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

    def teach(self):
        self.log_action("Начало лекции")
        students_list = self.students if hasattr(self, 'students') else []
        if students_list:
            self.notify_students("Началась лекция по алгоритмам")
        return "Провожу лекции по алгоритмам"

    def assess_progress(self, progress: Dict[str, float]):
            self.log_action("Оценка прогресса студентов")
            return super().assess_progress(progress)
    
    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data.update({
            'languages': self.__languages
        })
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ProgrammingCourse':
        start_date = date.fromisoformat(data['start_date'])
        end_date = date.fromisoformat(data['end_date'])
        
        course = cls(
            title=data['title'],
            start_date=start_date,
            end_date=end_date,
            instructor=data['instructor'],
            students=data['students'],
            topics=data['topics'],
            languages=data.get('languages', [])
        )
        
        return course