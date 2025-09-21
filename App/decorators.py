from functools import wraps
from App.exceptions import PermissionDeniedError  
from App.context import get_current_user

def check_permissions(required_permission: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user = get_current_user()
            
            if user is None:
                raise PermissionDeniedError("Пользователь не аутентифицирован")
            
            # Проверяем права доступа
            if required_permission == 'edit_course':
                if not has_edit_permission(user):
                    raise PermissionDeniedError("Недостаточно прав для редактирования курса")
            
            elif required_permission == 'assess_progress':
                if not has_assess_permission(user):
                    raise PermissionDeniedError("Недостаточно прав для оценки прогресса")
            
            # Передаем все аргументы включая self
            return func(*args, **kwargs)
        return wrapper
    return decorator

def has_edit_permission(user) -> bool:
    return hasattr(user, 'role') and user.role in ['admin', 'instructor']

def has_assess_permission(user) -> bool:
    return hasattr(user, 'role') and user.role in ['admin', 'instructor', 'assistant']

