class InvalidDateError(Exception):
    """Исключение, вызываемое когда дата окончания курса раньше даты начала"""
    pass

class PermissionDeniedError(Exception):
    """Исключение, вызываемое при отсутствии необходимых прав доступа"""
    pass

class CourseNotFoundError(Exception):
    """Исключение, вызываемое когда курс не найден"""
    pass