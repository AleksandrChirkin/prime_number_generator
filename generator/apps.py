from django.apps import AppConfig


class GeneratorConfig(AppConfig):
    """Конфигурация части приложения, ответственной за генерирование сертификатов простых чисел"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'generator'
