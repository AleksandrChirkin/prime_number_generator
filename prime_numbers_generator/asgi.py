import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'prime_numbers_generator.settings')

application = get_asgi_application()
