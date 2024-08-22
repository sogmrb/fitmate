from django import forms
from django.forms import ModelForm, Form
from meal.models import UserFoodEntry


class UserFoodEntryForm(ModelForm):
    serving = forms.ChoiceField(choices=[], required=True)

    class Meta:
        model = UserFoodEntry
        fields = (
            "quantity",
            "meal_time",
        )


class FoodSearchForm(Form):
    query = forms.CharField(max_length=100)

