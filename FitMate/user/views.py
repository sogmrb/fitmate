
from django.urls import NoReverseMatch, reverse
from django.utils import timezone

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View

from .forms import ProfileInfoForm, CreateAccountForm, MyLoginForm
from .models import WeightHistory
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import auth


class RegisterView(View):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('core:dashboard')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        profile_form = ProfileInfoForm()
        account_form = CreateAccountForm()
        return render(request, 'user/welcome_page.html', {
            'profile_form': profile_form,
            'account_form': account_form
        })

    def post(self, request, *args, **kwargs):
        profile_form = ProfileInfoForm(request.POST)
        account_form = CreateAccountForm(request.POST)
        if profile_form.is_valid():
            if account_form.is_valid():
                user = account_form.save()
                profile = profile_form.save(commit=False)
                if profile.goal not in ['weight_loss', 'muscle_gain']:
                    profile.weekly_weight_gain_or_loss_goal = 0
                profile.user = user
                profile.save()
                date = timezone.now().date()
                WeightHistory.objects.create(profile=profile, date_logged=date, weight=profile.weight)

                login(request, user)
                return JsonResponse({'success': True, 'redirect_url': reverse('core:dashboard')})
            else:
                return JsonResponse({
                    'success': False,
                    'errors': account_form.errors,
                    'non_field_errors': account_form.non_field_errors(),
                })

        return render(request, 'user/welcome_page.html', {
            'profile_form': profile_form,
            'account_form': account_form
        })


class MyLoginView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('core:dashboard')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = MyLoginForm()
        redirect_to = request.GET.get('redirect_to', None)
        return render(request, 'user/login.html', {"form": form, "redirect_to": redirect_to})

    def post(self, request, *args, **kwargs):
        form = MyLoginForm(request, data=request.POST)

        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                redirect_to = request.POST.get('redirect_to', None)
                print(redirect_to)
                auth.login(request, user)
                if redirect_to:
                    try:
                        return redirect(redirect_to)
                    except NoReverseMatch:
                        return redirect("core:dashboard")
                else:
                    return redirect("core:dashboard")
            else:
                form.add_error(None, "Invalid username or password")

        return render(request, 'user/login.html', {"form": form})


class LogoutView(View):

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("user:my_login")
