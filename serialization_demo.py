from datetime import date
from App.dto.User import User
from App.dto.course.ProgrammingCourse import ProgrammingCourse
from App.dto.course.DesignCourse import DesignCourse
from App.dto.Platform import Platform
from App.dto.Address import Address
from App.context import set_current_user
from App.serializers import JSONSerializer

def demonstrate_serialization():
    print("=== ДЕМОНСТРАЦИЯ СЕРИАЛИЗАЦИИ И ДЕСЕРИАЛИЗАЦИИ ===\n")
    
    admin_user = User("admin_user", "admin")
    instructor_user = User("instructor_user", "instructor")
    
    set_current_user(admin_user)

    platform_address = Address("example.com", "https://www.example.com")
    platform = Platform("Моя образовательная платформа", platform_address)
    
    set_current_user(instructor_user)
    programming_course = ProgrammingCourse(
        title="Python Programming",
        start_date=date(2024, 1, 1),
        end_date=date(2024, 12, 31),
        instructor="John Doe",
        students=["student1", "student2"],
        topics=["Basic", "OOP", "Web"],
        languages=["Python"]
    )
    
    design_course = DesignCourse(
        title="Graphic Design",
        start_date=date(2024, 2, 1),
        end_date=date(2024, 6, 30),
        instructor="Jane Smith",
        students=["student3", "student4"],
        topics=["Color Theory", "Typography"],
        tools=["Photoshop", "Illustrator"]
    )
    
    set_current_user(admin_user)
    platform.add_course(programming_course)
    platform.add_course(design_course)
    
    print("1. Исходная платформа:")
    print(f"   {platform}")
    print(f"   Курсов: {len(platform.get_courses())}")
    print()
    
    # Сериализуем в JSON
    print("2. Сериализация в JSON:")
    serializer = JSONSerializer()
    json_data = serializer.serialize(platform)
    print(f"   Данные платформы сохранены в JSON")
    print(f"   Размер JSON: {len(json_data)} символов")
    print()
    
    # Сохраняем в файл
    print("3. Сохранение в файл:")
    with open('platform_data.json', 'w', encoding='utf-8') as f:
        f.write(json_data)
    print("   Данные сохранены в файл 'platform_data.json'")
    print()
    
    # Загружаем из файла
    print("4. Загрузка из файла:")
    with open('platform_data.json', 'r', encoding='utf-8') as f:
        loaded_json = f.read()
    print("   Данные загружены из файла")
    print()
    
    # Восстанавливаем объект
    print("5. Восстановление объекта:")
    restored_platform = serializer.deserialize(loaded_json, Platform)
    print(f"   Платформа восстановлена: {restored_platform}")
    print(f"   Курсов восстановлено: {len(restored_platform.get_courses())}")
    print()
    
    print("6. Проверка восстановленных данных:")
    for i, course in enumerate(restored_platform.get_courses()):
        print(f"   Курс {i+1}: {course}")
        print(f"   Тип: {type(course).__name__}")
        print()
    
    print("7. Проверка методов восстановленных объектов:")
    try:
        programming_course_restored = restored_platform.get_courses()[0]
        result = programming_course_restored.teach()
        print(f"   Метод teach() работает: {result}")
    except Exception as e:
        print(f"   Ошибка при вызове метода: {e}")

if __name__ == "__main__":
    demonstrate_serialization()