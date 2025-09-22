from abc import ABC, abstractmethod
from datetime import date
from typing import List, Dict, Any
import logging
from App.metaclasses import CourseMeta
from App.dto.ProgressAssessors import ProgressAssessor
from App.decorators import check_permissions
from App.exceptions import InvalidDateError  

# Настройка логирования для курсов
course_logger = logging.getLogger('course')

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
        course_logger.info(f"Создан курс: {title} с {len(students)} студентами")

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
        course_logger.info(f"Изменено название курса: {self.__title} -> {value}")
        self.__title = value

    @property
    def start_date(self) -> date:
        return self.__start_date
    
    @start_date.setter
    @check_permissions('edit_course')
    def start_date(self, value: date):
        # Добавлена проверка дат
        # Устанавливает дату начала курса.
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
            error_msg = f"Дата начала {value} не может быть позже даты окончания {self.__end_date}"
            course_logger.error(error_msg)
            raise InvalidDateError(error_msg)
        course_logger.info(f"Изменена дата начала курса: {self.__start_date} -> {value}")
        self.__end_date = value

    @property
    def instructor(self) -> str:
        # Возвращает имя инструктора.
        return self.__instructor
    
    @instructor.setter
    @check_permissions('edit_course')
    def instructor(self, value: str):
        # Устанавливает имя инструктора.
        course_logger.info(f"Изменен инструктор курса: {self.__instructor} -> {value}")
        self.__instructor = value

    @property
    def students(self) -> List[str]:
        return self.__students
    
    @students.setter
    @check_permissions('edit_course')
    def students(self, value: List[str]):
        # Устанавливает список студентов.
        course_logger.info(f"Изменен список студентов: {len(self.__students)} -> {len(value)} студентов")
        self.__students = value

    @property
    def topics(self) -> List[str]:
        return self.__topics
    
    @topics.setter
    @check_permissions('edit_course')
    def topics(self, value: List[str]):
        # Устанавливает список тем курса.
        course_logger.info(f"Изменен список тем курса: {len(self.__topics)} -> {len(value)} тем")
        self.__topics = value

    @check_permissions('edit_course')
    def update_course_program(self, new_topics: List[str]):
        """Обновляет программу курса"""
        course_logger.info(f"Обновлена программа курса: {len(self.__topics)} -> {len(new_topics)} тем")
        self.topics = new_topics

    # --------- Методы сравнения ---------
    def __eq__(self, other: "Course") -> bool:
        # Сравнивает курсы по количеству студентов.
        if not isinstance(other, Course):
            return NotImplemented
        return len(self.__students) == len(other.students)

    def __lt__(self, other: "Course") -> bool:
        # Сравнивает курсы по количеству студентов (меньше).
        if not isinstance(other, Course):
            return NotImplemented
        return len(self.__students) < len(other.students)

    def __gt__(self, other: "Course") -> bool:
        # Сравнивает курсы по количеству студентов (больше).
        if not isinstance(other, Course):
            return NotImplemented
        return len(self.__students) > len(other.students)

    def __le__(self, other: "Course") -> bool:
        """Сравнивает курсы по количеству студентов (меньше или равно)."""
        if not isinstance(other, Course):
            return NotImplemented
        return len(self.__students) <= len(other.students)

    def __ge__(self, other: "Course") -> bool:
        """Сравнивает курсы по количеству студентов (больше или равно)."""
        if not isinstance(other, Course):
            return NotImplemented
        return len(self.__students) >= len(other.students)

    def compare_by_duration(self, other: "Course") -> int:
        """Сравнивает курсы по продолжительности (в днях)."""
        if not isinstance(other, Course):
            raise TypeError("Можно сравнивать только с объектами Course")

        # вычисляем продолжительность в днях для каждого курса
        self_duration = (self.__end_date - self.__start_date).days
        other_duration = (other.end_date - other.start_date).days

        if self_duration < other_duration:
            return -1
        elif self_duration > other_duration:
            return 1
        else:
            return 0

    #--------- Метод, выводящий строку о курсе
    def __str__(self)->str:
        return f"Курс: {self.__title}, Преподаватель: {self.__instructor}"
    
    #--------- Метод less than - выдает меньше ли у этого курса студентов чем у другого
    # аргументы: второй курс для сравнения
    # def __lt__(self, other: "Course")->bool:
    #     return len(self.__students) < len(other.__students)
    #
    # # --------- Метод greater than - выдает меньше ли у этого курса студентов чем у другого
    # # аргументы: второй курс для сравнения
    # def __gt__(self, other: "Course") -> bool:
    #     return len(self.__students) > len(other.__students)
    #
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