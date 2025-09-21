# serialization_demo.py
from datetime import date
from App.dto.User import User
from App.dto.course.ProgrammingCourse import ProgrammingCourse
from App.dto.course.DesignCourse import DesignCourse
from App.dto.Platform import Platform
from App.dto.Address import Address
from App.serializer import save_to_file, load_from_file

def demonstrate_serialization():

    print("=== ДЕМОНСТРАЦИЯ СЕРИАЛИЗАЦИИ И ДЕСЕРИАЛИЗАЦИИ ===\n")
    
    # Создаем пользователей
    admin_user = User("admin_user", "admin")
    instructor_user = User("instructor_user", "instructor")
    
    # Создаем адрес для платформы
    platform_address = Address("example.com", "https://www.example.com")
    
    # Создаем платформу
    platform = Platform("Моя образовательная платформа", platform_address, admin_user)
    
    # Создаем курсы
    programming_course = ProgrammingCourse(
        title="Python Programming",
        start_date=date(2024, 1, 1),
        end_date=date(2024, 12, 31),
        instructor="John Doe",
        students=["student1", "student2"],
        topics=["Basic", "OOP", "Web"],
        languages=["Python"],
        current_user=instructor_user
    )
    
    design_course = DesignCourse(
        title="Graphic Design",
        start_date=date(2024, 2, 1),
        end_date=date(2024, 6, 30),
        instructor="Jane Smith",
        students=["student3", "student4"],
        topics=["Color Theory", "Typography"],
        tools=["Photoshop", "Illustrator"],
        current_user=instructor_user
    )
    
    # Добавляем курсы на платформу
    platform.add_course(programming_course)
    platform.add_course(design_course)
    
    print("1. Исходная платформа:")
    print(f"   {platform}")
    print(f"   Курсов: {len(platform.get_courses())}")
    print()
    
    # Сериализуем в словарь
    print("2. Сериализация в словарь:")
    platform_dict = platform.to_dict()
    print(f"   Данные платформы сохранены в словарь")
    print(f"   Размер словаря: {len(str(platform_dict))} символов")
    print()
    
    # Сохраняем в файл
    print("3. Сохранение в файл:")
    save_to_file(platform_dict, 'platform_data.json')
    print("   Данные сохранены в файл 'platform_data.json'")
    print()
    
    # Загружаем из файла
    print("4. Загрузка из файла:")
    loaded_data = load_from_file('platform_data.json')
    print("   Данные загружены из файла")
    print()
    
    # Восстанавливаем объект
    print("5. Восстановление объекта:")
    restored_platform = Platform.from_dict(loaded_data)
    print(f"   Платформа восстановлена: {restored_platform}")
    print(f"   Курсов восстановлено: {len(restored_platform.get_courses())}")
    print()
    
    print("6. Проверка восстановленных данных:")
    for i, course in enumerate(restored_platform.get_courses()):
        print(f"   Курс {i+1}: {course}")
        print(f"   Тип: {type(course).__name__}")
        if hasattr(course, 'current_user') and course.current_user:
            print(f"   Пользователь: {course.current_user}")
        print()
    
    print("7. Проверка методов восстановленных объектов:")
    try:
        # Пытаемся вызвать методы восстановленных объектов
        programming_course_restored = restored_platform.get_courses()[0]
        result = programming_course_restored.teach()
        print(f"   Метод teach() работает: {result}")
    except Exception as e:
        print(f"   Ошибка при вызове метода: {e}")

if __name__ == "__main__":
    demonstrate_serialization()