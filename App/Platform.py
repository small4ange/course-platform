from App.Course import Course
from App.Address import Address
from typing import List

# ------------ Класс для списка курсов и методов управления ими
class Platform:
    def __init__(self, name: str, address: Address):
        self.__name = name # название платформы
        self.__address = address  # адрес создаётся вместе с платформой
        self.__courses: List["Course"] = []  # список курсов

    @property
    def name(self) -> str:
        return self.__name
    @property
    def address(self) -> Address:
        return self.__address

    #---------- Метод добавления курса на платформу
    def add_course(self, course: "Course") -> None:
        self.__courses.append(course)

    # ---------- Метод удаления курса с платформы
    def remove_course(self, course: "Course") -> None:
        if course in self.__courses:
            self.__courses.remove(course)

    # --------- Метод получения списка всех курсов
    def get_courses(self) -> List["Course"]:
        return self.__courses

    # ---------- Метод получения топ-N курсов по кол-ву студентов
    def get_top_courses(self, n: int) -> List["Course"]:
        return sorted(self.__courses, key=lambda c: len(c.students), reverse=True)[:n]

    # ---------- Вывод данных платформы в строку
    def __str__(self):
        return f"Платформа: {self.__name}, Адрес: {self.__address}, Количество курсов: {len(self.__courses)}"