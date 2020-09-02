from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django_crispy_bulma import forms as bulma_forms
from django_crispy_bulma.layout import Field, Submit, Row, Column
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
    first_name = forms.CharField(empty_value="John", label="Prénom")
    last_name = forms.CharField(empty_value="Doe", label="Nom")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(
                Column(Field("username")),
                Column(Field("email")),
            ),
            Row(
                Column(Field("first_name")),
                Column(Field("last_name")),
            ),
            Field("password1"),
            Field("password2"),
            Submit("submit", "Confirmer l'inscription", css_class="is-primary")
        )

    def save(self, commit=True):
        print("##### SAVE #####")
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            self.save_m2m()
        return user

    def clean_email(self):
        print("### CLEAN EMAIL ###")
        if User.objects.filter(email=self.cleaned_data["email"]).exists():
            raise ValidationError(self.fields["email"].error_messages["exists"])
        return self.cleaned_data["email"]
