from functools import wraps
from App.exceptions import PermissionDeniedError

def check_permissions(required_role: str):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            # Проверяем, есть ли у объекта информация о пользователе
            if not hasattr(self, 'current_user') or not self.current_user:
                raise PermissionDeniedError("Пользователь не аутентифицирован")
            
            # Проверяем права доступа
            if self.current_user.role != required_role:
                raise PermissionDeniedError(
                    f"Недостаточно прав. Требуется роль: {required_role}"
                )
            
            return func(self, *args, **kwargs)
        return wrapper
    return decorator