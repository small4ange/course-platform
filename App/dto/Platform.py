from App.dto.course.Course import Course
from App.dto.Address import Address
from typing import List
from App.decorators import check_permissions
from App.exceptions import CourseNotFoundError  
from App.dto.course.ProgrammingCourse import ProgrammingCourse
from App.dto.course.DesignCourse import DesignCourse
from App.dto.course.ScienceCourse import ScienceCourse
import logging


platform_logger = logging.getLogger('platform')

# ------------ Класс для списка курсов и методов управления ими
class Platform:
    def __init__(self, name: str, address: Address):
        self.__name = name
        self.__address = address
        self.__courses: List["Course"] = []
        platform_logger.info(f"Создана платформа: {name}")

    @property
    def name(self) -> str:
        return self.__name
    
    @property
    def address(self) -> Address:
        return self.__address

    #---------- Метод добавления курса на платформу
    @check_permissions('edit_course')
    def add_course(self, course: "Course") -> None:
        platform_logger.info(f"Добавлен курс '{course.title}' на платформу '{self.__name}'")
        self.__courses.append(course)

    # ---------- Метод удаления курса с платформы
    @check_permissions('edit_course')
    def remove_course(self, course: "Course") -> None:
        if course not in self.__courses:
            platform_logger.warning(f"Попытка удаления несуществующего курса: {course.title}")
            raise CourseNotFoundError("Курс не найден на платформе")
        platform_logger.info(f"Удален курс '{course.title}' с платформы '{self.__name}'")
        self.__courses.remove(course)

    # --------- Метод получения списка всех курсов
    def get_courses(self) -> List["Course"]:
        return self.__courses

    # ---------- Метод получения топ-N курсов по кол-ву студентов
    def get_top_courses(self, n: int) -> List["Course"]:
        platform_logger.info(f"Получен топ-{n} курсов по количеству студентов")
        return sorted(self.__courses, key=lambda c: len(c.students), reverse=True)[:n]

    # ---------- Вывод данных платформы в строку
    def __str__(self):
        return f"Платформа: {self.__name}, Адрес: {self.__address}, Количество курсов: {len(self.__courses)}"
    
    def to_dict(self) -> dict:
        return {
            'name': self.__name,
            'address': self.__address.to_dict(),
            'courses': [course.to_dict() for course in self.__courses]
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Platform':
        address = Address.from_dict(data['address'])
        platform = cls(
            name=data['name'],
            address=address
        )
        
        platform._Platform__courses = []
        
        for course_data in data['courses']:
            from App.serializers import JSONSerializer
            course = JSONSerializer._create_course_from_dict(course_data)
            platform._Platform__courses.append(course)
        
        return platform

    def save_to_file(self, filename: str) -> None:
        #Сохраняет платформу в файл JSON
        import json
        from App.serializers import DateTimeEncoder
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2, cls=DateTimeEncoder)

    @classmethod
    def load_from_file(cls, filename: str) -> 'Platform':
        #Загружает платформу из файла JSON
        import json
        
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return cls.from_dict(data)
    
    def get_course_by_index(self, index: int) -> "Course":
        if index < 0 or index >= len(self.__courses):
            platform_logger.warning(f"Попытка получения курса по несуществующему индексу: {index}")
            raise CourseNotFoundError(f"Курс с индексом {index} не найден")
        return self.__courses[index]