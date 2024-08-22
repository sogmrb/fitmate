from datetime import timedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views import View

from user.models import Profile
from .forms import UserExerciseEntryForm
from .models import UserExerciseEntry
import ast


def total_daily_stats(entries):
    pass


class IndexView(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        selected_date = request.GET.get('date')
        profile = get_object_or_404(Profile, user=request.user)
        name = profile.name
        if selected_date:
            date = timezone.datetime.strptime(selected_date, '%Y-%m-%d').date()
        else:
            date = timezone.now().date()

        next_date = None
        prev_date = None
        if date >= timezone.now().date():
            prev_date = (date - timedelta(days=1)).strftime('%Y-%m-%d')
        else:
            prev_date = (date - timedelta(days=1)).strftime('%Y-%m-%d')
            next_date = (date + timedelta(days=1)).strftime('%Y-%m-%d')

        user_exercise_entries = UserExerciseEntry.objects.filter(user=user, date=date)

        if not user_exercise_entries.exists():
            return render(request, "exercise/index.html",
                          {"message": "No entries for this day.", 'date': date, 'prev_date': prev_date,
                           'next_date': next_date, 'name': name})

        daily_stats = total_daily_stats(user_exercise_entries)
        print(daily_stats)
        return render(request, "exercise/index.html",
                      {
                          "exercise_entries": user_exercise_entries,
                          'date': date,
                          'prev_date': prev_date,
                          'next_date': next_date,
                          'daily_stats': daily_stats,
                          'name': name,
                      })


class AddView(View):
    def get(self, request, *args, **kwargs):
        date = request.GET.get('date')
        form = UserExerciseEntryForm()

        return render(request, "exercise/add.html", {"form": form, "date": date})

    def post(self, request, *args, **kwargs):
        user = request.user
        date = request.GET.get('date')
        form = UserExerciseEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = user
            if date is None:
                date = timezone.now().date()
            entry.date = date
            entry.save()
            return redirect('exercise:index')
        return render(request, "exercise/add.html", {"form": form, "date": date})



class DetailView(View):
    pass


class EditView(View):
    pass


class DeleteView(View):
    pass


class SearchView(View):
    pass