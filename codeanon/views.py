from django.conf import settings
from django.views.generic import FormView
from .forms import RegisterForm


class RegisterView(FormView):
    template_name = "register.html"
    form_class = RegisterForm
    success_url = settings.LOGIN_REDIRECT_URL
