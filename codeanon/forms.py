from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Button
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django_crispy_bulma import forms as bulma_forms
from wagtail.users.forms import UserCreationForm

User = get_user_model()


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )

    email = bulma_forms.EmailField(
        required=True,
        label="Email",
        error_messages={"exists": "Cette adresse email existe déjà"},
    )
    first_name = forms.CharField(empty_value="John")
    last_name = forms.CharField(empty_value="Doe")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = "layout col-light columns"
        self.helper.layout = Layout(
            Field("username", placeholder="Nom d'utilisateur"),
            Field("first_name", placeholder="Prénom", css_class="column is-half"),
            Field("last_name", placeholder="Nom", css_class="column is-half"),
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
            Button("submit", "S'enregistrer", type="submit", css_class="col-light"),
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data["email"]).exists():
            raise ValidationError(self.fields["email"].error_messages["exists"])
        return self.cleaned_data["email"]
