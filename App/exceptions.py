class InvalidDateError(Exception):
    #Исключение для невалидных дат
    pass

class PermissionDeniedError(Exception):
    #Исключение для отсутствия прав доступа
    pass

class CourseNotFoundError(Exception):
    #Исключение для отсутствия курса
    pass