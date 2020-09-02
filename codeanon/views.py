from crispy_forms.helper import FormHelper
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.views.generic import FormView
from django_crispy_bulma.layout import Layout, Field, Submit

from .forms import RegisterForm


class RegisterView(FormView):
    template_name = "crispy_form.html"
    form_class = RegisterForm
    success_url = settings.LOGIN_REDIRECT_URL

    def form_valid(self, form):
        self.object = form.save()
        messages.add_message(self.request, messages.INFO,
                             "Vous avez bien été inscrit. Veuillez maintenant vous connecter.")
        return super().form_valid(form)


class LoginView(auth_views.LoginView):
    template_name = "crispy_form.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        form.helper = FormHelper()
        form.helper.form_class = "layout col-light"
        form.helper.layout = Layout(
            Field("username", placeholder="Username"),
            Field("password", placeholder="Password"),
            Submit("submit", "Se connecter", css_class="is-primary")
        )

        return form
