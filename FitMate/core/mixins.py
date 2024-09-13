from django.contrib.auth.mixins import LoginRequiredMixin


class CustomLoginRequiredMixin(LoginRequiredMixin):
    login_url = '/login/'  # Default login URL
    redirect_field_name = 'redirect_to'

