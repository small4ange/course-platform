from App.dto.course.Course import Course
from App.dto.Address import Address
from typing import List, Dict, Any
from App.decorators import check_permissions
from App.exceptions import PermissionDeniedError, CourseNotFoundError

# ------------ Класс для списка курсов и методов управления ими
class Platform:
    def __init__(self, name: str, address: Address, current_user=None):
        self.__name = name 
        self.__address = address  # адрес создаётся вместе с платформой
        self.__courses: List[Course] = [] 
        self.current_user = current_user 

    @property
    def name(self) -> str:
        return self.__name
    @property
    def address(self) -> Address:
        return self.__address

    #---------- Метод добавления курса на платформу
    @check_permissions('admin')
    def add_course(self, course: Course) -> None:
        self.__courses.append(course)

    # ---------- Метод удаления курса с платформы
    @check_permissions('admin')
    def remove_course(self, course: Course) -> None:
        if course in self.__courses:
            self.__courses.remove(course)
        else:
            raise CourseNotFoundError("Курс не найден на платформе")

    # --------- Метод получения списка всех курсов
    def get_courses(self) -> List[Course]:
        return self.__courses

    # ---------- Метод получения топ-N курсов по кол-ву студентов
    def get_top_courses(self, n: int) -> List[Course]:
        return sorted(self.__courses, key=lambda c: len(c.students), reverse=True)[:n]

    # ---------- Метод поиска курса по названию
    def find_course_by_title(self, title: str) -> Course:
        for course in self.__courses:
            if course.title == title:
                return course
        raise CourseNotFoundError(f"Курс с названием '{title}' не найден")

    # ---------- Метод получения курса по индексу
    def get_course_by_index(self, index: int) -> Course:
        try:
            return self.__courses[index]
        except IndexError:
            raise CourseNotFoundError(f"Курс с индексом {index} не найден")

    # ---------- Вывод данных платформы в строку
    def __str__(self):
        return f"Платформа: {self.__name}, Адрес: {self.__address}, Количество курсов: {len(self.__courses)}"

    def to_dict(self) -> Dict[str, Any]:
        """Преобразует объект платформы в словарь"""
        return {
            'name': self.__name,
            'address': {
                'domain': self.__address.domain,
                'url': self.__address.url
            },
            'courses': [course.to_dict() for course in self.__courses],
            'current_user': {
                'username': self.current_user.username,
                'role': self.current_user.role
            } if self.current_user else None
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Platform':
        """Создает объект платформы из словаря"""
        from App.dto.Address import Address
        from App.dto.User import User
        
        # Создаем адрес
        address_data = data['address']
        address = Address(address_data['domain'], address_data['url'])
        
        # Создаем пользователя
        current_user = None
        if data.get('current_user'):
            current_user = User(data['current_user']['username'], data['current_user']['role'])
        
        # Создаем платформу
        platform = cls(data['name'], address, current_user)
        
        # Восстанавливаем курсы
        for course_data in data['courses']:
            course = cls._create_course_from_dict(course_data)
            platform.__courses.append(course)
        
        return platform

    @staticmethod
    def _create_course_from_dict(data: Dict[str, Any]) -> Course:
        """Создает объект курса соответствующего типа из словаря"""
        course_type = data['type']
        
        if course_type == 'DesignCourse':
            from App.dto.course.DesignCourse import DesignCourse
            return DesignCourse.from_dict(data)
        elif course_type == 'ProgrammingCourse':
            from App.dto.course.ProgrammingCourse import ProgrammingCourse
            return ProgrammingCourse.from_dict(data)
        elif course_type == 'ScienceCourse':
            from App.dto.course.ScienceCourse import ScienceCourse
            return ScienceCourse.from_dict(data)
        else:
            raise ValueError(f"Неизвестный тип курса: {course_type}")