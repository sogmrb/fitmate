import json
import os
from django.core.management.base import BaseCommand
from exercise.models import Exercise

class Command(BaseCommand):
    help = 'Import exercises from a JSON file into the database'

    def handle(self, *args, **kwargs):
        json_file_path = os.path.join(os.path.dirname(__file__), 'exercises.json')

        # Open and read the JSON file
        with open(json_file_path, 'r') as file:
            exercises = json.load(file)

        # Iterate over the data and create Exercise objects
        for exercise_data in exercises:
            exercise, created = Exercise.objects.get_or_create(
                name=exercise_data['name'],
                defaults={
                    'MET_value': exercise_data['MET_value'],
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Added exercise: {exercise.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Exercise already exists: {exercise.name}"))
