# App/main.py
from datetime import date
from dto.User import User
from dto.Platform import Platform
from dto.Address import Address
from context import set_current_user, get_current_user
from exceptions import InvalidDateError, PermissionDeniedError, CourseNotFoundError
from dto.course.CourseFactory import CourseFactory
from logging_config import setup_logging
import logging

# Настройка логирования
log_file = setup_logging()
logger = logging.getLogger('main')


class EducationalPlatformDemo:
    """
    Демонстрационный класс для образовательной платформы.

    Показывает основные возможности системы:
    - Создание и управление курсами
    - Работу с правами доступа
    - Логирование и уведомления
    - Обработку исключений
    """

    def __init__(self):
        """Инициализирует демонстрационный класс."""
        self.platform = None
        self.admin_user = User("admin_user", "admin", "admin@example.com")
        self.instructor_user = User("instructor_user", "instructor", "instructor@example.com")
        self.student_user = User("student_user", "student", "student@example.com")
        logger.info("Демонстрационный класс инициализирован")

    def demonstrate_platform_usage(self):
        """
        Основная демонстрация работы платформы.

        Включает все основные функции системы:
        - Создание платформы и курсов
        - Управление данными
        - Анализ данных
        - Логирование и уведомления
        - Обработку исключений
        - Сравнение курсов
        """
        logger.info("Начало демонстрации работы платформы")
        print("🎓 ДЕМОНСТРАЦИЯ РАБОТЫ ОБРАЗОВАТЕЛЬНОЙ ПЛАТФОРМЫ")
        print("=" * 60)
        print(f"📝 Логи записываются в файл: {log_file}")
        print()

        self._create_platform()
        self._create_and_add_courses()
        self._manage_course_data()
        self._analyze_data()
        self._demonstrate_logging_notifications()
        # self._handle_exceptions()
        self._demonstrate_course_comparison()

        print("🎉 ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА УСПЕШНО!")
        print("=" * 60)
        logger.info("Демонстрация завершена успешно")

    def _create_platform(self):
        """Создает образовательную платформу."""
        logger.info("Создание платформы")
        print("\n1. СОЗДАНИЕ ПЛАТФОРМЫ")
        print("-" * 40)

        set_current_user(self.admin_user)
        platform_address = Address("edu-platform.com", "https://www.edu-platform.com")
        self.platform = Platform("Моя образовательная платформа", platform_address)

        print(f"   ✅ Платформа создана: {self.platform}")
        logger.info(f"Платформа создана: {self.platform.name}")

    def _create_and_add_courses(self):
        """Создает и добавляет курсы на платформу."""
        logger.info("Создание и добавление курсов")
        print("\n2. СОЗДАНИЕ И ДОБАВЛЕНИЕ КУРСОВ (через CourseFactory)")
        print("-" * 60)

        set_current_user(self.admin_user)

        # Создание курсов разных типов через фабрику
        programming_course = CourseFactory.create_course(
            "programming",
            "Python Programming",
            date(2024, 1, 15),
            date(2024, 6, 15),
            "John Doe",
            ["student1", "student2", "student3", "student4"],
            ["Basic", "OOP", "Web", "Databases", "Testing"],
            languages=["Python", "SQL", "JavaScript"]
        )

        design_course = CourseFactory.create_course(
            "design",
            "Graphic Design",
            date(2024, 2, 1),
            date(2024, 7, 1),
            "Jane Smith",
            ["student5", "student6", "student7"],
            ["Color Theory", "Typography", "Layout", "Branding"],
            tools=["Photoshop", "Illustrator", "Figma", "InDesign"]
        )

        science_course = CourseFactory.create_course(
            "science",
            "Data Science",
            date(2024, 3, 1),
            date(2024, 8, 1),
            "Dr. Brown",
            ["student8", "student9"],
            ["Statistics", "Machine Learning", "Data Visualization", "Big Data"],
            field=["Data Science", "AI", "Machine Learning"]
        )

        # Добавление курсов на платформу
        self.platform.add_course(programming_course)
        self.platform.add_course(design_course)
        self.platform.add_course(science_course)

        print("   ✅ Курсы созданы и добавлены на платформу:")
        for i, course in enumerate(self.platform.get_courses(), 1):
            print(f"      {i}. {course}")

        logger.info(f"Добавлено {len(self.platform.get_courses())} курсов на платформу")

    def _manage_course_data(self):
        """Управляет данными курсов (редактирование, удаление)."""
        logger.info("Управление данными курсов")
        print("\n3. УПРАВЛЕНИЕ ДАННЫМИ КУРСОВ")
        print("-" * 40)

        set_current_user(self.admin_user)
        courses = self.platform.get_courses()

        if courses:
            # Редактирование данных курса через сеттеры
            programming_course = courses[0]

            print("   📝 Редактирование данных курса программирования:")
            print(f"      Старое название: {programming_course.title}")
            programming_course.title = "Advanced Python Programming"
            print(f"      Новое название: {programming_course.title}")

            print(f"      Старые темы: {programming_course.topics}")
            programming_course.topics.append("Advanced Algorithms")
            print(f"      Новые темы: {programming_course.topics}")

    def _analyze_data(self):
        """Анализирует данные платформы."""
        logger.info("Анализ данных платформы")
        print("\n4. АНАЛИЗ ДАННЫХ ПЛАТФОРМЫ")
        print("-" * 40)

        # Получение списка всех курсов
        print("   📊 Все курсы платформы:")
        all_courses = self.platform.get_courses()
        for i, course in enumerate(all_courses, 1):
            print(f"      {i}. {course.title} - {len(course.students)} студентов")

        # Поиск топ-N курсов по количеству студентов
        if all_courses:
            print("\n   🏆 Топ курсы по количеству студентов:")
            top_n = min(2, len(all_courses))
            top_courses = self.platform.get_top_courses(top_n)
            for i, course in enumerate(top_courses, 1):
                print(f"      {i}. {course.title} - {len(course.students)} студентов")

    def _demonstrate_logging_notifications(self):
        """Демонстрирует работу логирования и уведомлений."""
        logger.info("Демонстрация логирования и уведомлений")
        print("\n5. ЛОГИРОВАНИЕ И УВЕДОМЛЕНИЯ")
        print("-" * 40)

        set_current_user(self.instructor_user)
        courses = self.platform.get_courses()

        if courses:
            course = courses[0]

            # Использование миксинов для логирования
            print("   📝 Логирование действий:")
            course.log_action("Начало демонстрации работы миксинов")
            course.log_action("Проверка функциональности уведомлений")

            # Использование миксинов для уведомлений
            print("   🔔 Отправка уведомлений студентам:")
            course.notify_students("Завтра состоится дополнительное занятие")
            course.notify_students("Не забудьте выполнить домашнее задание")

    def _handle_exceptions(self):
        """Демонстрирует обработку исключений."""
        logger.info("Демонстрация обработки исключений")
        print("\n6. ОБРАБОТКА ИСКЛЮЧЕНИЙ")
        print("-" * 40)

        # Обработка исключения при создании курса с некорректными датами
        print("   ⚠️ Попытка создания курса с некорректными датами:")
        try:
            invalid_course = CourseFactory.create_course(
                "programming",
                "Invalid Course",
                date(2024, 12, 31),
                date(2024, 1, 1),
                "John Doe",
                ["student1"],
                ["Topic1"],
                languages=["Python"]
            )
            print("      ❌ Курс создан (не должно было произойти)")
        except InvalidDateError as e:
            print(f"      ✅ Правильно обработано: {e}")

        # Обработка исключения при отсутствии прав доступа
        print("\n   ⚠️ Попытка редактирования курса студентом:")
        set_current_user(self.student_user)
        try:
            courses = self.platform.get_courses()
            if courses:
                courses[0].title = "Недозволенное изменение"
                print("      ❌ Изменение прошло (не должно было произойти)")
        except PermissionDeniedError as e:
            print(f"      ✅ Правильно обработано: {e}")

    def _demonstrate_course_comparison(self):
        """Демонстрирует методы сравнения курсов."""
        logger.info("Демонстрация методов сравнения курсов")
        print("\n7. СРАВНЕНИЕ КУРСОВ")
        print("-" * 40)

        courses = self.platform.get_courses()
        if len(courses) >= 2:
            course1, course2 = courses[0], courses[1]

            print("   🔍 Сравнение курсов по количеству студентов:")
            print(f"      {course1.title}: {len(course1.students)} студентов")
            print(f"      {course2.title}: {len(course2.students)} студентов")

            # Использование методов сравнения
            print(f"      Курс 1 == Курс 2: {course1 == course2}")
            print(f"      Курс 1 < Курс 2: {course1 < course2}")
            print(f"      Курс 1 > Курс 2: {course1 > course2}")
            print(f"      Курс 1 <= Курс 2: {course1 <= course2}")
            print(f"      Курс 1 >= Курс 2: {course1 >= course2}")

            print("\n   📅 Сравнение по продолжительности:")
            duration1 = (course1.end_date - course1.start_date).days
            duration2 = (course2.end_date - course2.start_date).days
            print(f"      {course1.title}: {duration1} дней")
            print(f"      {course2.title}: {duration2} дней")

            comparison = course1.compare_by_duration(course2)
            if comparison < 0:
                print(f"      {course1.title} короче чем {course2.title}")
            elif comparison > 0:
                print(f"      {course1.title} длиннее чем {course2.title}")
            else:
                print(f"      Курсы имеют одинаковую продолжительность")


def main():
    """
    Точка входа в программу.

    Запускает демонстрацию работы образовательной платформы.
    """
    try:
        demo = EducationalPlatformDemo()
        demo.demonstrate_platform_usage()
    except Exception as e:
        logger.error(f"Ошибка при выполнении демонстрации: {e}")
        print(f"❌ Произошла ошибка: {e}")


if __name__ == "__main__":
    main()