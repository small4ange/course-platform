class User:

    def __init__(self, username: str, role: str):
        """
        Инициализация пользователя
        
        Args:
            username: Имя пользователя
            role: Роль пользователя ('student', 'instructor', 'admin')
        """
        self.username = username
        self.role = role
    
    def __str__(self) -> str:
        return f"User(username='{self.username}', role='{self.role}')"
    
    def __repr__(self) -> str:
        return self.__str__()