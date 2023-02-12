from csv import reader

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        Ingredient.objects.all().delete()
        with open(
            'data/ingredients.csv', 'r', encoding='UTF-8'
        ) as ingredients:
            for line in reader(ingredients):
                if len(line) == 2:
                    Ingredient.objects.get_or_create(
                        name=line[0],
                        measurement_unit=line[1],
                    )