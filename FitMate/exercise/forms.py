from django import forms
from django.forms import ModelForm, Form
from .models import UserExerciseEntry


class UserExerciseEntryManualForm(ModelForm):
    class Meta:
        model = UserExerciseEntry
        fields = (
            "name",
            "category",
            "duration",
            "burned_calories",
            "notes",
        )


class UserExerciseEntryForm(ModelForm):
    class Meta:
        model = UserExerciseEntry
        fields = (
            "category",
            "duration",
            "notes",
        )


class ExerciseSearchForm(Form):
    query = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Search for an exercise...'}))
