from django.contrib import admin
from .models import Exercise,UserExerciseEntry
# Register your models here.
admin.site.register(Exercise)
admin.site.register(UserExerciseEntry)
