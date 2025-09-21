# exception_demo.py
from datetime import date
from App.dto.User import User
from App.dto.course.ProgrammingCourse import ProgrammingCourse
from App.dto.Platform import Platform
from App.dto.Address import Address
from App.exceptions import InvalidDateError, PermissionDeniedError, CourseNotFoundError

def demonstrate_exceptions():

    print("=== ДЕМОНСТРАЦИЯ ПОЛЬЗОВАТЕЛЬСКИХ ИСКЛЮЧЕНИЙ ===\n")
    
    # Создаем пользователей
    admin_user = User("admin_user", "admin")
    student_user = User("student_user", "student")
    
    # Создаем адрес для платформы
    platform_address = Address("example.com", "https://www.example.com")
    platform = Platform("Моя платформа", platform_address, admin_user)
    
    print("1. Тестирование InvalidDateError:")
    try:
        # Попытка создать курс с невалидными датами
        invalid_course = ProgrammingCourse(
            title="Invalid Course",
            start_date=date(2024, 1, 1),
            end_date=date(2023, 12, 31), 
            instructor="John Doe",
            students=[],
            topics=[],
            languages=["Python"],
            current_user=admin_user
        )
        print("   Курс создан успешно")
    except InvalidDateError as e:
        print(f"   Ошибка: {e}")
    print()
    
    print("2. Тестирование PermissionDeniedError:")
    try:
        # Студент пытается создать платформу (не имеет прав админа)
        student_platform = Platform("Студентская", platform_address, student_user)
        # Попытка добавить курс без прав
        course = ProgrammingCourse(
            title="Python Course",
            start_date=date(2024, 1, 1),
            end_date=date(2024, 12, 31),
            instructor="John Doe",
            students=[],
            topics=[],
            languages=["Python"],
            current_user=student_user
        )
        student_platform.add_course(course)
        print("   Курс добавлен успешно")
    except PermissionDeniedError as e:
        print(f"   Ошибка: {e}")
    print()
    
    print("3. Тестирование CourseNotFoundError:")
    try:
        # Попытка найти несуществующий курс
        platform.find_course_by_title("Несуществующий курс")
        print("   Курс найден")
    except CourseNotFoundError as e:
        print(f"   Ошибка: {e}")
    
    try:
        # Попытка получить курс по неверному индексу
        platform.get_course_by_index(999)
        print("   Курс получен")
    except CourseNotFoundError as e:
        print(f"   Ошибка: {e}")
    print()
    
    print("4. Тестирование сеттеров дат:")
    try:
        # Создаем валидный курс
        course = ProgrammingCourse(
            title="Valid Course",
            start_date=date(2024, 1, 1),
            end_date=date(2024, 12, 31),
            instructor="John Doe",
            students=[],
            topics=[],
            languages=["Python"],
            current_user=admin_user
        )
        
        # Попытка установить невалидную дату окончания
        course.end_date = date(2023, 12, 31)  
        print("   Дата установлена успешно")
    except InvalidDateError as e:
        print(f"   Ошибка при установке даты: {e}")

if __name__ == "__main__":
    demonstrate_exceptions()