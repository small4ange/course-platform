from abc import ABC, abstractmethod
from datetime import date
from typing import List, Dict
from App.metaclasses import CourseMeta

# ------ Абстрактный класс для наследования всеми классами курсов
class Course(ABC, metaclass=CourseMeta):
    def __init__(self, title: str, start_date: date, end_date: date, instructor: str, students: List[str], topics: List[str]):
            self.__title = title # Название курса
            self.__start_date = start_date # Дата начала курса
            self.__end_date = end_date # Дата окончания курса
            self.__instructor = instructor # Преподаватель курса
            self.__students = students # Список студентов
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
        self.__start_date = value

    @property
    def end_date(self) -> date:
        return self.__end_date
    @end_date.setter
    def end_date(self, value: date):
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


