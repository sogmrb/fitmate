from django.utils import timezone
from django.db import models
from user.models import User


class Exercise(models.Model):
    name = models.CharField(max_length=100)
    MET_value = models.FloatField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class UserExerciseEntry(models.Model):
    CARDIO = "cardio"
    STRENGTH = "strength"
    FLEXIBILITY = "flexibility"

    CATEGORY_CHOICES = ((CARDIO, "Cardio"), (STRENGTH, "Strength Training"), (FLEXIBILITY, "Flexibility"),)

    name = models.CharField(max_length=100)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, default=None, blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    duration = models.IntegerField(default=0)
    burned_calories = models.IntegerField(default=0)
    date = models.DateField(default=timezone.now)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.name}"

    class Meta:
        ordering = ('date',)
