from django import forms
from .config import (
    MAX_USERNAME_LENGTH, MAX_PASSWORD_LENGTH, MAX_TITLE_LENGTH,
    MAX_DESCRIPTION_LENGTH, MAX_TAGS_LENGTH, MAX_TAGS, MAX_OPTION_LENGTH
)

class Login(forms.Form):
    username = forms.CharField(max_length=MAX_USERNAME_LENGTH)
    password = forms.CharField(
        max_length=MAX_PASSWORD_LENGTH, widget=forms.PasswordInput()
    )


class SignUp(forms.Form):
    username = forms.CharField(max_length=MAX_USERNAME_LENGTH)
    password = forms.CharField(
        max_length=MAX_PASSWORD_LENGTH, widget=forms.PasswordInput()
    )
    confirm_password = forms.CharField(
        max_length=MAX_PASSWORD_LENGTH, widget=forms.PasswordInput()
    )


class CreatePost(forms.Form):
    title = forms.CharField(max_length=MAX_TITLE_LENGTH)
    description_one = forms.CharField(max_length=MAX_DESCRIPTION_LENGTH)
    description_two = forms.CharField(max_length=MAX_DESCRIPTION_LENGTH)
    image_one = forms.ImageField(required=False)
    image_two = forms.ImageField(required=False)
    tags = forms.CharField(max_length=MAX_TAGS_LENGTH)


class TagSearch(forms.Form):
    tag = forms.CharField(max_length=MAX_TAGS_LENGTH//MAX_TAGS)


class VoteOption(forms.Form):
    vote_option = forms.ChoiceField(choices=(
        ('1', '1'), ('2', '2')
    ))