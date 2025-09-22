# App/logging_config.py
import logging
import os
from datetime import datetime


def setup_logging():
    """
    Настраивает систему логирования для приложения.

    Логи записываются в файл и выводятся в консоль.
    """
    # Создаем папку для логов если ее нет
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Формат логов
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'

    # Базовый уровень логирования
    logging.basicConfig(level=logging.INFO, format=log_format, datefmt=date_format)

    # Файловый обработчик
    log_filename = f"{log_dir}/educational_platform_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    file_handler = logging.FileHandler(log_filename, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(log_format, datefmt=date_format))

    # Консольный обработчик
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(log_format, datefmt=date_format))

    # Добавляем обработчики к корневому логгеру
    root_logger = logging.getLogger()
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    # Устанавливаем уровень логирования для разных компонентов
    logging.getLogger('course').setLevel(logging.INFO)
    logging.getLogger('platform').setLevel(logging.INFO)
    logging.getLogger('user').setLevel(logging.INFO)

    return log_filename