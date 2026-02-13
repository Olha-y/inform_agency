from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms.widgets import CheckboxSelectMultiple

from .models import Newspaper
from django.forms import (
    ModelForm,
    ModelMultipleChoiceField,
)

User = get_user_model()


class RedactorExperienceUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ("years_of_experience",)

    def clean_license_number(self):
        years_of_experience = self.cleaned_data["years_of_experience"]

        if not isinstance(years_of_experience, int):
            raise ValidationError(
                "Years of experience must be positive integer"
            )
        return years_of_experience


class RedactorCreateForm(
    UserCreationForm,
    RedactorExperienceUpdateForm
):
    class Meta:
        model = User
        fields = (
            "username",
            "years_of_experience",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        )


class RedactorSearchForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by username"}),
    )


class NewspaperForm(ModelForm):
    publishers = ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Newspaper
        fields = "__all__"


class NewspaperSearchForm(forms.Form):
    title = forms.CharField(
        max_length=100,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by title"}),
    )


class NewspaperUpdateForm(ModelForm):
    class Meta:
        model = Newspaper
        fields = ("title", "content",)

    def clean_license_number(self):
        title = self.cleaned_data["title"]
        content = self.cleaned_data["content"]
        return title, content
