class User:
    #Класс для представления пользователя системы
    
    def __init__(self, username: str, role: str, email: str = None):
        self.username = username
        self.role = role  # 'admin', 'instructor', 'assistant', 'student'
        self.email = email
        self.permissions = self._get_permissions_by_role(role)
    
    def _get_permissions_by_role(self, role: str) -> list:
        permissions_map = {
            'admin': ['edit_course', 'assess_progress', 'manage_users'],
            'instructor': ['edit_course', 'assess_progress'],
            'assistant': ['assess_progress'],
            'student': []
        }
        return permissions_map.get(role, [])
    
    def has_permission(self, permission: str) -> bool:
        return permission in self.permissions
    
    def __str__(self):
        return f"User(username={self.username}, role={self.role})"
    
    def __repr__(self):
        return self.__str__()