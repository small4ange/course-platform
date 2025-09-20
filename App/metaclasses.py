from abc import ABCMeta

class CourseMeta(ABCMeta):
    registry = {}

    def __new__(cls, name, bases, attrs):
        new_class = super().__new__(cls, name, bases, attrs)
        if name != "Course":  # не регистрируем сам абстрактный класс
            cls.registry[name] = new_class
        return new_class
