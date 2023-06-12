from django import forms
from .config import (
    USERNAME_LENGTH, PASSWORD_LENGTH, TITLE_LENGTH,
    DESCRIPTION_LENGTH, TAGS_LENGTH
)

class Login(forms.Form):
    username = forms.CharField(max_length=USERNAME_LENGTH)
    password = forms.CharField(
        max_length=PASSWORD_LENGTH, widget=forms.PasswordInput()
    )

class CreatePost(forms.Form):
    title = forms.CharField(max_length=TITLE_LENGTH)
    description_one = forms.CharField(max_length=DESCRIPTION_LENGTH)
    description_two = forms.CharField(max_length=DESCRIPTION_LENGTH)
    image_one = forms.ImageField(required=False)
    image_two = forms.ImageField(required=False)
    tags = forms.CharField(max_length=TAGS_LENGTH)