from django import forms
from django.forms import ModelForm, Form
from .models import UserExerciseEntry


class UserExerciseEntryForm(ModelForm):

    class Meta:
        model = UserExerciseEntry
        fields = (
            "name",
            "category",
            "duration",
            "burned_calories",
            "notes",
        )

