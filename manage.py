import logging
import os
import sys
import threading
from typing import Any

from generator import Generator
from signal import signal, SIGTERM


def signal_handler(signum: int, frame: Any) -> None:
    """Обработчик сигнала остановки SIGTERM"""
    sys.stdout.close()


def start_generator() -> None:
    """Запустить генератор сертификатов"""
    logging.basicConfig(format='%(message)s', level=logging.INFO, stream=sys.stdout)
    generator_thread = threading.Thread(target=Generator().generate)
    logging.info("Запускаем генератор...")
    generator_thread.start()
    logging.info("Генератор запущен!")


def main() -> None:
    """Запуск Django-приложения"""
    signal(SIGTERM, signal_handler)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'prime_numbers_generator.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    if 'runserver' in sys.argv:
        sys.stdout = open('generatorOutput.log', mode='a+')
        sys.stderr = sys.stdout
        start_generator()
    execute_from_command_line(sys.argv)


# точка входа
if __name__ == '__main__':
    main()
