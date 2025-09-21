from datetime import date
from App.dto.User import User
from App.dto.course.ProgrammingCourse import ProgrammingCourse
from App.dto.course.DesignCourse import DesignCourse
from App.dto.course.ScienceCourse import ScienceCourse
from App.dto.Platform import Platform
from App.dto.Address import Address
from App.exceptions import PermissionDeniedError

def demonstrate_permissions():

    print("=== ДЕМОНСТРАЦИЯ СИСТЕМЫ ПРАВ ДОСТУПА ===\n")
    
    # Создаем пользователей с разными ролями
    admin_user = User("admin_user", "admin")
    instructor_user = User("instructor_user", "instructor")
    student_user = User("student_user", "student")
    
    # Создаем адрес для платформы
    platform_address = Address("example.com", "https://www.example.com")
    
    print("1. Создание платформы с правами администратора:")
    platform = Platform("Моя образовательная платформа", platform_address, admin_user)
    print(f"   Платформа создана: {platform}")
    print()
    
    print("2. Создание курсов с разными пользователями:")
    
    # Курс программирования с инструктором
    programming_course = ProgrammingCourse(
        title="Python Programming",
        start_date=date(2023, 9, 1),
        end_date=date(2023, 12, 31),
        instructor="John Doe",
        students=["student1", "student2"],
        topics=["Basic", "OOP", "Web"],
        languages=["Python"],
        current_user=instructor_user
    )
    print(f"   Создан курс: {programming_course}")
    
    # Курс дизайна со студентом (не должно быть прав)
    design_course = DesignCourse(
        title="Graphic Design",
        start_date=date(2023, 10, 1),
        end_date=date(2024, 2, 28),
        instructor="Jane Smith",
        students=["student1", "student3"],
        topics=["Color Theory", "Typography", "Layout"],
        tools=["Photoshop", "Illustrator"],
        current_user=student_user
    )
    print(f"   Создан курс: {design_course}")
    print()
    
    print("3. Попытка преподавания с разными правами:")
    
    # Инструктор пытается преподавать - должно работать
    print("   Инструктор пытается преподавать:")
    try:
        result = programming_course.teach()
        print(f"   Успех: {result}")
    except PermissionDeniedError as e:
        print(f"   Ошибка: {e}")
    
    # Студент пытается преподавать - должно вызвать ошибку
    print("   Студент пытается преподавать:")
    try:
        result = design_course.teach()
        print(f"   Успех: {result}")
    except PermissionDeniedError as e:
        print(f"   Ошибка: {e}")
    print()
    
    print("4. Попытка оценки прогресса:")
    
    progress_data = {"student1": 85.5, "student2": 92.0}
    
    # Инструктор оценивает прогресс - должно работать
    print("   Инструктор оценивает прогресс:")
    try:
        completion_rate = programming_course.assess_progress(progress_data)
        print(f"   Средний процент завершения: {completion_rate:.1f}%")
    except PermissionDeniedError as e:
        print(f"   Ошибка: {e}")
    print()
    
    print("5. Управление курсами на платформе:")
    
    # Админ добавляет курс - должно работать
    print("   Админ добавляет курс на платформу:")
    try:
        platform.add_course(programming_course)
        print(f"   Курс добавлен. Всего курсов: {len(platform.get_courses())}")
    except PermissionDeniedError as e:
        print(f"   Ошибка: {e}")
    
    # Студент пытается добавить курс - должно вызвать ошибку
    student_platform = Platform("Студентская платформа", platform_address, student_user)
    print("   Студент пытается добавить курс:")
    try:
        student_platform.add_course(design_course)
        print(f"   Курс добавлен. Всего курсов: {len(student_platform.get_courses())}")
    except PermissionDeniedError as e:
        print(f"   Ошибка: {e}")
    print()
    
    print("6. Проверка методов без проверки прав (должны работать всегда):")
    
    # Эти методы доступны всем
    courses = platform.get_courses()
    print(f"   Получение списка курсов: {len(courses)} курс(ов)")
    
    course_info = str(programming_course)
    print(f"   Информация о курсе: {course_info}")

if __name__ == "__main__":
    demonstrate_permissions()