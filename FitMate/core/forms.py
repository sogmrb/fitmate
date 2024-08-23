from django import forms
from django.forms import ModelForm
from user.models import WeightHistory


class LogWeightForm(ModelForm):
    class Meta:
        model = WeightHistory
        fields = ('weight',)

