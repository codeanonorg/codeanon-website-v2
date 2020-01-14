from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
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

    email = forms.EmailField(
        required=True,
        label="Email",
        error_messages={"exists": "Cette adresse email existe déjà"},
    )
    first_name = forms.CharField(empty_value="John")
    last_name = forms.CharField(empty_value="Doe")

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
