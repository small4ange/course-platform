import logging

# Настройка логирования: сообщения будут выводиться в консоль
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

class LoggingMixin:
    def log_action(self, message: str):
        """Логирование действий курса"""
        if hasattr(self, "title"):
            logging.info(f"[{self.title}] {message}")
        else:
            logging.info(f"[Курс без названия] {message}")

class NotificationMixin:
    def notify_students(self, message: str):
        """Отправка уведомлений студентам"""
        if hasattr(self, "students") and self.students:
            for student in self.students:
                # В реальной программе здесь можно сделать отправку email/telegram
                print(f"Уведомление для {student}: {message}")
        else:
            print("Студенты не найдены, уведомления не отправлены")
