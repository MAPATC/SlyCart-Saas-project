import json
from django.core.management.base import BaseCommand
from config.api import api  # объект NinjaAPI

class Command(BaseCommand):
    help = "Экспорт OpenAPI схемы в JSON файл"

    def handle(self, *args, **options):
        schema = api.get_openapi_schema() # Генерируем схему
        with open("openapi.json", "w", encoding="utf-8") as f:
            json.dump(schema, f, indent=2, ensure_ascii=False)
        self.stdout.write(self.style.SUCCESS("Схема успешно сохранена в openapi.json"))
