#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

import logging
import os
import sys
import threading

from generator import Generator


def main():
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
        msg_format = "%(asctime)s: %(message)s"
        logging.basicConfig(format=msg_format, level=logging.INFO, datefmt="%H:%M:%S")
        generator_thread = threading.Thread(target=Generator().generate)
        logging.info("Starting generator...")
        generator_thread.start()
        logging.info("Generator started!")
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
