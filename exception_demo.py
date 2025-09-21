from datetime import date
from App.dto.User import User
from App.dto.course.ProgrammingCourse import ProgrammingCourse
from App.dto.Platform import Platform
from App.dto.Address import Address
from App.context import set_current_user
from App.exceptions import InvalidDateError, PermissionDeniedError, CourseNotFoundError

def demonstrate_exceptions():
    print("=== ДЕМОНСТРАЦИЯ ПОЛЬЗОВАТЕЛЬСКИХ ИСКЛЮЧЕНИЙ ===\n")
    
    admin_user = User("admin_user", "admin")
    student_user = User("student_user", "student")
    
    platform_address = Address("example.com", "https://www.example.com")
    
    print("1. Тестирование:")
    try:
        set_current_user(admin_user)
        invalid_course = ProgrammingCourse(
            title="Invalid Course",
            start_date=date(2024, 1, 1),
            end_date=date(2023, 12, 31), 
            instructor="John Doe",
            students=[],
            topics=[],
            languages=["Python"]
        )
        print("   Курс создан успешно")
    except InvalidDateError as e:
        print(f"   Ошибка: {e}")
    print()
    
    print("2. Тестирование:")
    try:
        # Студент пытается создать курс (не имеет прав)
        set_current_user(student_user)
        course = ProgrammingCourse(
            title="Python Course",
            start_date=date(2024, 1, 1),
            end_date=date(2024, 12, 31),
            instructor="John Doe",
            students=[],
            topics=[],
            languages=["Python"]
        )
        print("   Курс создан успешно")
    except PermissionDeniedError as e:
        print(f"   Ошибка: {e}")
    print()
    
    print("3. Тестирование:")
    try:
        # Создаем платформу и пытаемся найти несуществующий курс
        set_current_user(admin_user)
        platform = Platform("Моя платформа", platform_address)
        
        # Попытка найти несуществующий курс
        platform.get_course_by_index(0)
        print("   Курс найден")
    except CourseNotFoundError as e:
        print(f"   Ошибка: {e}")
    print()
    
    print("4. Тестирование сеттеров дат:")
    try:
        # Создаем валидный курс
        set_current_user(admin_user)
        course = ProgrammingCourse(
            title="Valid Course",
            start_date=date(2024, 1, 1),
            end_date=date(2024, 12, 31),
            instructor="John Doe",
            students=[],
            topics=[],
            languages=["Python"]
        )
        
        # Попытка установить невалидную дату окончания
        course.end_date = date(2023, 12, 31)  
        print("   Дата установлена успешно")
    except InvalidDateError as e:
        print(f"   Ошибка при установке даты: {e}")

if __name__ == "__main__":
    demonstrate_exceptions()