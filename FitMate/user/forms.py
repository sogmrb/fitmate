from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput, TextInput

from .models import Profile, WeightHistory


class ProfileInfoForm(forms.ModelForm):
    name = forms.CharField(
        max_length=120,
        widget=forms.TextInput(attrs={
            'class': 'name-form-control',
            'placeholder': 'Enter your name'
        }),
        required=True
    )
    GOAL_CHOICES = [
        ('weight_loss', 'Weight Loss'),
        ('muscle_gain', 'Muscle Gain'),
        ('health', 'Healthier Lifestyle'),
        ('anxiety', 'Manage Anxiety'),
    ]
    goal = forms.ChoiceField(
        choices=GOAL_CHOICES,
        widget=forms.RadioSelect(),
    )

    ACTIVITY_CHOICES = [
        ('sedentary', 'Sedentary (little or no exercise)'),
        ('light', 'Lightly active (light exercise/sports 1-3 days/week)'),
        ('moderate', 'Moderately active (moderate exercise/sports 3-5 days/week)'),
        ('active', 'Active (hard exercise/sports 6-7 days a week)'),
        ('very_active', 'Very active (very hard exercise/sports & physical job)'),
    ]
    activity_level = forms.ChoiceField(
        choices=ACTIVITY_CHOICES,
        widget=forms.RadioSelect(),
    )

    SEX_CHOICES = [('male', 'Male'), ('female', 'Female'), ('other', 'Other')]
    sex = forms.ChoiceField(choices=SEX_CHOICES, widget=forms.RadioSelect)
    age = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'profile-form-control', 'placeholder': 'Age', 'min': '16', 'max': '100'}, )
    )
    height = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'profile-form-control', 'placeholder': 'Height', 'min': '130', 'max': '230'}, )
    )
    weight = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'profile-form-control', 'placeholder': 'Weight', 'min': '30', 'max': '300'})
    )
    goal_weight = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'profile-form-control', 'placeholder': 'Goal Weight', 'min': '30', 'max': '300'})
    )

    class Meta:
        model = Profile
        fields = ('name', 'goal', 'activity_level', 'sex', 'age', 'height', 'weight', 'goal_weight')


class CreateAccountForm(UserCreationForm):
    username = forms.CharField(max_length=15, help_text='Required. 15 characters or fewer.',
                               widget=TextInput(attrs={'class': 'signup-form-control', }))
    email = forms.EmailField(
        help_text="Required. Please enter a valid email address.",
        widget=TextInput(attrs={'class': 'signup-form-control', })
    )

    password1 = forms.CharField(widget=PasswordInput(attrs={'class': 'signup-form-control', }))
    password2 = forms.CharField(widget=PasswordInput(attrs={'class': 'signup-form-control', }))

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already taken')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already taken')
        return email

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class MyLoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class': 'login-form-control', 'placeholder': 'Username'}, ))
    password = forms.CharField(widget=PasswordInput(attrs={'class': 'login-form-control', 'placeholder': 'Password'}, ))


class LogWeightForm(forms.ModelForm):
    class Meta:
        model = WeightHistory
        fields = ('weight',)


class WeeklyGainOrLossForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('weekly_weight_gain_or_loss_goal', )
        widgets = {
            'weekly_weight_gain_or_loss_goal': forms.NumberInput(attrs={
                'step': '0.1',
                'min': '0.1',
                'max': '1.0',
            }),
        }
