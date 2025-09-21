from abc import ABC, abstractmethod
from datetime import date
from typing import List, Dict, Any
from App.metaclasses import CourseMeta
from App.exceptions import InvalidDateError

# ------ Абстрактный класс для наследования всеми классами курсов
class Course(ABC, metaclass=CourseMeta):
    def __init__(self, title: str, start_date: date, end_date: date, instructor: str, students: List[str], topics: List[str]):
            # Проверяем валидность дат
            if end_date < start_date:
                raise InvalidDateError("Дата окончания курса не может быть раньше даты начала")
            
            self.__title = title 
            self.__start_date = start_date 
            self.__end_date = end_date 
            self.__instructor = instructor 
            self.__students = students 
            self.__topics = topics # Список тем

    #--------- Подсчет процента завершения курса в зависимости от его типа (переопределяется всеми классами с разными типами курсов)
    # аргументы: progress - словарь [студент, процент пройденных тем]
    @abstractmethod
    def calculate_completion_rate(self, progress) -> float:
        pass

    #---------Геттеры сеттеры
    @property
    def title(self)->str:
        return self.__title
    @title.setter
    def title(self, value: str):
        self.__title = value

    @property
    def start_date(self) -> date:
        return self.__start_date
    @start_date.setter
    def start_date(self, value: date):
        # Проверяем валидность даты при установке
        if value > self.__end_date:
            raise InvalidDateError("Дата начала не может быть позже даты окончания")
        self.__start_date = value

    @property
    def end_date(self) -> date:
        return self.__end_date
    @end_date.setter
    def end_date(self, value: date):
        # Проверяем валидность даты при установке
        if value < self.__start_date:
            raise InvalidDateError("Дата окончания не может быть раньше даты начала")
        self.__end_date = value

    @property
    def instructor(self) -> str:
        return self.__instructor
    @instructor.setter
    def instructor(self, value: str):
        self.__instructor = value

    @property
    def students(self) -> List[str]:
        return self.__students
    @students.setter
    def students(self, value: List[str]):
        self.__students = value

    @property
    def topics(self) -> List[str]:
        return self.__topics
    @topics.setter
    def topics(self, value: List[str]):
        self.__topics = value

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
        """Преобразует объект курса в словарь"""
        return {
            'type': self.__class__.__name__,
            'title': self.__title,
            'start_date': self.__start_date,
            'end_date': self.__end_date,
            'instructor': self.__instructor,
            'students': self.__students,
            'topics': self.__topics
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Course':
        """Создает объект курса из словаря"""
        # Этот метод будет переопределен в дочерних классах
        raise NotImplementedError("Метод from_dict должен быть реализован в дочерних классах")