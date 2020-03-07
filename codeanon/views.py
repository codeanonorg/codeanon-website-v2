from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, HTML
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.views.generic import FormView

from .forms import RegisterForm


class RegisterView(FormView):
    template_name = "crispy_form.html"
    form_class = RegisterForm
    success_url = settings.LOGIN_REDIRECT_URL


class LoginView(auth_views.LoginView):
    template_name = "crispy_form.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        form.helper = FormHelper()
        form.helper.form_class = "layout col-light"
        form.helper.layout = Layout(
            Field("username", placeholder="Username"),
            Field("password", placeholder="Password"),
            HTML('<button class="btn btn-primary" type="submit">Login</button>'),
        )

        return form
