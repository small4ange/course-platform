from abc import ABC, abstractmethod
from typing import Dict, Any

# Класс для представления запроса на изменение
class ChangeRequest:
    def __init__(self, change_type: str, change_data: Dict[str, Any], requester: str):
        self.change_type = change_type # изменения: "материалы", "структура", "любые"
        self.change_data = change_data # данные изменения
        self.requester = requester # кто запросил
        self.approved = False # был ли запрос одобрен
        self.approved_by = None # какой обработчик одобрил

# Абстракный класс обработчика
class Handler(ABC):
    def __init__(self, successor = None):
        self._successor = successor # следующий обработчик в цепочке

    @abstractmethod
    def can_handle(self, request: ChangeRequest) -> bool: # проверяет, может ли этот обработчик решить запрос
        pass
    @abstractmethod
    def handle_request(self, request: ChangeRequest) -> bool: # обрабатывает запрос или передает дальше
        pass

class InstructorHandler(Handler): #Обработчик преподавателя, он может одобрить изменения в материалах
    def can_handle(self, request: ChangeRequest) -> bool:
        return request.change_type == "materials"

    def handle_request(self, request: ChangeRequest) -> bool:
        if self.can_handle(request):
            print(f"Преподаватель одобрил изменения в материалх от {request.requester}")
            request.approved = True
            request.approved_by = "Instructor"
            return True
        elif self._successor: # Если есть следующий обработчик
            return self._successor.handle_request(request) # Передаем далее другому обработчику
        return False # Никто не можеть одобрить изменения


class MethodologyDepartmentHandler(Handler):  # Обработчик методического отдела, он может одобрить изменения в структуре
    def can_handle(self, request: ChangeRequest) -> bool:
        return request.change_type == "structure"

    def handle_request(self, request: ChangeRequest) -> bool:
        if self.can_handle(request):
            print(f"Методический отдел одобрил изменения в структуре от {request.requester}")
            request.approved = True
            request.approved_by = "MethodologyDepartment"
            return True
        elif self._successor:  # Если есть следующий обработчик
            return self._successor.handle_request(request)  # Передаем далее другому обработчику
        return False  # Никто не можеть одобрить изменения

class ManagementHandler(Handler):  # Обработчик руководства, оно может одобрить изменения в материалах
    def can_handle(self, request: ChangeRequest) -> bool:
        return True # Может одобрить все

    def handle_request(self, request: ChangeRequest) -> bool:
        if self.can_handle(request):
            print(f"Руководство одобрило изменения от {request.requester}")
            request.approved = True
            request.approved_by = "Management"
            return True
        return False  # Никто не можеть одобрить изменения