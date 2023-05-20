#!/usr/bin/env python3

import logging
import os
import sys
import threading

from generator import Generator
from signal import signal, SIGTERM


def signal_handler(signum, frame):
    sys.stdout.close()


def start_generator():
    logging.basicConfig(format='%(message)s', level=logging.INFO, stream=sys.stdout)
    generator_thread = threading.Thread(target=Generator().generate)
    logging.info("Starting generator...")
    generator_thread.start()
    logging.info("Generator started!")

def main():
    signal(SIGTERM, signal_handler)
    if 'runserver' in sys.argv:
        sys.stdout = open('generatorOutput.log', mode='a+')
        sys.stderr = sys.stdout
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'prime_numbers_generator.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    # избегаем двойного запуска генератора
    if os.name == 'posix':
        procs = [(int(p), c) for p, c in [x.rstrip('\n').split(' ', 1) for x in os.popen('ps h -eo pid:1,command')]]
        if len([proc for proc in procs if str(proc[1]).endswith('manage.py runserver 8000')]) == 1:
            start_generator()
    elif os.name == 'nt':
        start_generator()
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
