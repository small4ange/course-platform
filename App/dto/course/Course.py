from abc import ABC, abstractmethod
from datetime import date
from typing import List, Dict, Any
from App.metaclasses import CourseMeta
from App.dto.ProgressAssessors import ProgressAssessor
from App.decorators import check_permissions
from App.exceptions import InvalidDateError  


# ------ Абстрактный класс для наследования всеми классами курсов
class Course(ABC, metaclass=CourseMeta):
    def __init__(self, title: str, start_date: date, end_date: date, instructor: str, students: List[str], topics: List[str]):
        if end_date < start_date:
            raise InvalidDateError("Дата окончания курса не может быть раньше даты начала")
            
        self.__title = title
        self.__start_date = start_date
        self.__end_date = end_date
        self.__instructor = instructor
        self.__students = students
        self.__topics = topics
        self.__progress_assessor = None


    @abstractmethod
    def create_progress_assessor(self) -> ProgressAssessor:
        """Фабричный метод для создания оценщика прогресса"""
        pass

    @check_permissions('assess_progress')
    def assess_progress(self, progress: Dict[str, float]) -> float:
        """Используем шаблонный метод для оценки прогресса"""
        if self.__progress_assessor is None:
            self.__progress_assessor = self.create_progress_assessor()
        return self.__progress_assessor.assess_progress(progress)

    #---------Геттеры сеттеры
    @property
    def title(self)->str:
        return self.__title
    
    @title.setter
    @check_permissions('edit_course')
    def title(self, value: str):
        self.__title = value

    @property
    def start_date(self) -> date:
        return self.__start_date
    
    @start_date.setter
    @check_permissions('edit_course')
    def start_date(self, value: date):
        # Добавлена проверка дат
        if hasattr(self, '_Course__end_date') and value > self.__end_date:
            raise InvalidDateError("Дата начала курса не может быть позже даты окончания")
        self.__start_date = value

    @property
    def end_date(self) -> date:
        return self.__end_date
    
    @end_date.setter
    @check_permissions('edit_course')
    def end_date(self, value: date):
        # Добавлена проверка дат
        if hasattr(self, '_Course__start_date') and value < self.__start_date:
            raise InvalidDateError("Дата окончания курса не может быть раньше даты начала")
        self.__end_date = value

    @property
    def instructor(self) -> str:
        return self.__instructor
    
    @instructor.setter
    @check_permissions('edit_course')
    def instructor(self, value: str):
        self.__instructor = value

    @property
    def students(self) -> List[str]:
        return self.__students
    
    @students.setter
    @check_permissions('edit_course')
    def students(self, value: List[str]):
        self.__students = value

    @property
    def topics(self) -> List[str]:
        return self.__topics
    
    @topics.setter
    @check_permissions('edit_course')
    def topics(self, value: List[str]):
        self.__topics = value

    @check_permissions('edit_course')
    def update_course_program(self, new_topics: List[str]):
        """Обновляет программу курса"""
        self.topics = new_topics

    #--------- Метод, выводящий строку о курсе
    def __str__(self)->str:
        return f"Курс: {self.__title}, Преподаватель: {self.__instructor}"
    
    #--------- Метод less than - выдает меньше ли у этого курса студентов чем у другого
    # аргументы: второй курс для сравнения
    def __lt__(self, other: "Course")->bool:
        return len(self.__students) < len(other.__students)

    # --------- Метод greater than - выдает меньше ли у этого курса студентов чем у другого
    # аргументы: второй курс для сравнения
    def __gt__(self, other: "Course") -> bool:
        return len(self.__students) > len(other.__students)
    
    def to_dict(self) -> Dict[str, Any]:
        #Преобразует объект курса в словарь
        return {
            'type': self.__class__.__name__,
            'title': self.__title,
            'start_date': self.__start_date.isoformat(),
            'end_date': self.__end_date.isoformat(),
            'instructor': self.__instructor,
            'students': self.__students,
            'topics': self.__topics
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Course':
        #Создает объект курса из словаря
        start_date = date.fromisoformat(data['start_date'])
        end_date = date.fromisoformat(data['end_date'])
        
        # Создаем базовый курс
        course = cls(
            title=data['title'],
            start_date=start_date,
            end_date=end_date,
            instructor=data['instructor'],
            students=data['students'],
            topics=data['topics']
        )
        
        return course