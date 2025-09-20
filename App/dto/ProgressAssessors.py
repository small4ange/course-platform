from abc import ABC, abstractmethod
from typing import Dict, List


# Общие функции для оценки прогресса
def validate_progress_data(progress_data: Dict[str, List[float]]) -> None:
    if not progress_data:
        raise ValueError("Данные прогресса не могут быть пустыми")
    for student, grades in progress_data.items():
        if not grades:
            raise ValueError(f"Нет оценок у студента {student}")
        for grade in grades:
            if grade < 0:
                raise ValueError(f"Отрицательная оценка {grade} у студента {student}")


def calculate_student_averages(progress_data: Dict[str, List[float]]) -> Dict[str, float]:
    student_averages = {}
    for student, grades in progress_data.items():
        if grades:
            student_averages[student] = sum(grades) / len(grades)
        else:
            student_averages[student] = 0.0
    return student_averages


# Абстрактный класс для шаблонного метода оценки прогресса
class ProgressAssessor(ABC):
    def __init__(self, course: "Course"):
        self.course = course

    def assess_progress(self, progress_data: Dict[str, List[float]]) -> Dict[str, float]:
        # Возвращает словарь: {студент: средний_балл}
        validate_progress_data(progress_data)  # 1. Валидация
        processed_results = self.process_student_grades(progress_data)  # 2. Обработка оценок
        student_averages = calculate_student_averages(processed_results)  # 3. Вычисление средних баллов
        final_assessments = self.apply_assessment(student_averages)  # 4. Применение оценки
        return final_assessments

    # Обработка оценок
    @abstractmethod
    def process_student_grades(self, progress_data: Dict[str, List[float]]) -> Dict[str, List[float]]:
        pass

    # Применение оценки
    @abstractmethod
    def apply_assessment(self, student_averages: Dict[str, float]) -> Dict[str, float]:
        pass


# Конкретные реализации
class ProgrammingProgressAssessor(ProgressAssessor):
    def process_student_grades(self, progress_data: Dict[str, List[float]]) -> Dict[str, List[float]]:
        """
        Для программирования: проверяем что оценки в диапазоне 0-1
        и преобразуем в проценты (0-100)
        """
        processed_grades = {}
        for student, grades in progress_data.items():
            # Проверяем что все оценки в диапазоне 0-1
            valid_grades = []
            for grade in grades:
                if 0 <= grade <= 1:
                    valid_grades.append(grade * 100)  # Преобразуем в проценты
                else:
                    raise ValueError(f"Некорректная оценка {grade} у студента {student}. Ожидается 0-1")
            processed_grades[student] = valid_grades
        return processed_grades

    def apply_assessment(self, student_averages: Dict[str, float]) -> Dict[str, float]:
        """
        Для программирования: возвращаем средний балл как есть (уже в процентах)
        """
        return student_averages


class DesignProgressAssessor(ProgressAssessor):
    def process_student_grades(self, progress_data: Dict[str, List[float]]) -> Dict[str, List[float]]:
        """
        Для дизайна: проверяем что оценки в диапазоне 0-100
        """
        processed_grades = {}
        for student, grades in progress_data.items():
            valid_grades = []
            for grade in grades:
                if 0 <= grade <= 100:
                    valid_grades.append(grade)
                else:
                    raise ValueError(f"Некорректная оценка {grade} у студента {student}. Ожидается 0-100")
            processed_grades[student] = valid_grades
        return processed_grades

    def apply_assessment(self, student_averages: Dict[str, float]) -> Dict[str, float]:
        """
        Для дизайна: возвращаем средний балл как есть (уже в процентах)
        """
        return student_averages


class ScienceProgressAssessor(ProgressAssessor):
    def process_student_grades(self, progress_data: Dict[str, List[float]]) -> Dict[str, List[float]]:
        """
        Для науки: нормализуем оценки к 100-балльной шкале
        Максимальный балл за задание = 10
        """
        processed_grades = {}
        max_score_per_task = 10  # Максимальный балл за одно задание

        for student, grades in progress_data.items():
            normalized_grades = []
            for grade in grades:
                if grade < 0:
                    raise ValueError(f"Отрицательная оценка {grade} у студента {student}")
                # Нормализуем к 100-балльной шкале
                normalized_grade = min(grade, max_score_per_task) / max_score_per_task * 100
                normalized_grades.append(normalized_grade)
            processed_grades[student] = normalized_grades
        return processed_grades

    def apply_assessment(self, student_averages: Dict[str, float]) -> Dict[str, float]:
        """
        Для науки: возвращаем средний балл как есть (уже в процентах)
        """
        return student_averages