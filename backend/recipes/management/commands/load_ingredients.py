from django.core.management.base import BaseCommand
import json

from recipes.models import Ingredient


class Command(BaseCommand):
    """Ingredients loader."""
    ERROR_MESSAGE = ('Not all the Ingredients been parsed, '
                     'The following ingredients were not loaded:')
    DUPLICATE_MESSAGE = ('The following elements were duplicated '
                         'an appropriate number times')
    ERROR_TEMPLATE = ('name: {name}, '
                      'measurement_unit: {unit}')
    help = "Load ingredients from JSON file"

    def add_arguments(self, parser):
        parser.add_argument('file_path',
                            type=str,
                            help='specify file to load')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        parsed_data = self.get_json_from_file(file_path)
        bulk, inconsistents, duplicates = self.prepare_bulk_create(
            parsed_data
        )
        Ingredient.objects.bulk_create(bulk)
        if len(inconsistents) >= 1:
            self.report_issue(inconsistents)
        if len(duplicates) >= 1:
            self.report_duplicates(duplicates)

    @staticmethod
    def get_json_from_file(file_path):
        with open(file_path, 'r', encoding='UTF-8') as file_object:
            return json.load(file_object)

    def prepare_bulk_create(self, parsed_data):
        not_parsed_data = []
        bulk_create = []
        duplicates = {}
        uniques = set()
        for ingredient in parsed_data:
            name = ingredient.get('name')
            measure_unit = ingredient.get('measurement_unit')
            if None in (name, measure_unit):
                not_parsed_data.append(
                    self.ERROR_TEMPLATE.format(name=name,
                                               unit=measure_unit)
                )
                continue
            if name in uniques:
                if name not in duplicates:
                    duplicates[name] = 0
                duplicates[name] += 1
                continue
            entry = Ingredient(name=name,
                               measurement_unit=measure_unit)
            bulk_create.append(entry)
            uniques.add(name)
        return bulk_create, not_parsed_data, duplicates

    def report_issue(self, not_parsed_ingredients):
        failed_elements = '\n'.join(not_parsed_ingredients)
        print(self.ERROR_MESSAGE)
        print(failed_elements)
        print()

    def report_duplicates(self, duplicates):
        print(self.DUPLICATE_MESSAGE)
        for name, count in duplicates.items():
            print(f'{name}:', count)
        print()
