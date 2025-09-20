from abc import ABC, abstractmethod
from typing import Dict


# Интерфейс для процесса обучения курса
class Teachable(ABC):
    @abstractmethod
    def teach(self):
        """Метод описывает процесс обучения курса"""
        pass

# Интерфейс для оценки прогресса студентов
class Assessable(ABC):
    @abstractmethod
    def assess_progress(self, progress: Dict[str, float]):
        """Метод для оценки прогресса студентов"""
        pass

    @abstractmethod
    def create_progress_assessor(self):
        """Фабричный метод для создания оценщика прогресса"""
        pass
