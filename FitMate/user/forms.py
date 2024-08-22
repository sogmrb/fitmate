from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput, TextInput

from user.models import Profile


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
        widget=forms.NumberInput(attrs={'class': 'profile-form-control', 'placeholder': 'Age'}, )
    )
    height = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'profile-form-control', 'placeholder': 'Height'}, )
    )
    weight = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'profile-form-control', 'placeholder': 'Weight'})
    )
    goal_weight = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'profile-form-control', 'placeholder': 'Goal Weight'})
    )

    class Meta:
        model = Profile
        fields = ('name', 'goal', 'activity_level', 'sex', 'age', 'height', 'weight', 'goal_weight')


class CreateAccountForm(UserCreationForm):
    username = forms.CharField(max_length=15, help_text='Required. 15 characters or fewer.')
    email = forms.EmailField(
        help_text="Required. Please enter a valid email address."
    )

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
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())
