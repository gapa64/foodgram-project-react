from django.core.management.base import BaseCommand
import json

from recipes.models import Ingredient


class Command(BaseCommand):
    """Ingredients loader."""
    ERROR_MESSAGE = ('Not all the Ingredients been parsed, '
                     'The following ingredients were not loaded:')
    help = "Load ingredients from JSON file"

    def add_arguments(self, parser):
        parser.add_argument('file_path',
                            type=str,
                            help='specify file to load')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        parsed_data = self.get_json_from_file(file_path)
        ingredients_bulk, not_parsed_ingredients = self.prepare_bulk_create(
            parsed_data
        )
        Ingredient.objects.bulk_create(ingredients_bulk)
        if len(not_parsed_ingredients) >= 1:
            self.report_issue(not_parsed_ingredients)

    @staticmethod
    def get_json_from_file(file_path):
        with open(file_path, 'r', encoding='UTF-8') as file_object:
            return json.load(file_object)

    @staticmethod
    def prepare_bulk_create(parsed_data):
        not_parsed_data = []
        bulk_create = []
        for ingredient in parsed_data:
            name = ingredient.get('name')
            measure_unit = ingredient.get('measurement_unit')
            if None in (name, measure_unit):
                not_parsed_data.append(f'name: {name}, '
                                       f'measurement_unit: {measure_unit}')
                continue
            entry = Ingredient(name=name,
                               measurement_unit=measure_unit)
            bulk_create.append(entry)
        return bulk_create, not_parsed_data

    def report_issue(self, not_parsed_ingredients):
        failed_elements = '\n'.join(not_parsed_ingredients)
        print(self.ERROR_MESSAGE)
        print(failed_elements)
