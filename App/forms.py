from django import forms
from .config import (
    MAX_USERNAME_LENGTH, MAX_PASSWORD_LENGTH, MAX_TITLE_LENGTH,
    MAX_DESCRIPTION_LENGTH, MAX_TAGS_LENGTH, MAX_TAG_LENGTH,
    MAX_MAIN_DESCRIPTION_LENTGH, MAX_COMMENT_LENGTH,
    MAX_BUTTON_LABEL_LENGTH
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
    main_description = forms.CharField(max_length=MAX_MAIN_DESCRIPTION_LENTGH)
    description_one = forms.CharField(max_length=MAX_DESCRIPTION_LENGTH, required=False)
    description_two = forms.CharField(max_length=MAX_DESCRIPTION_LENGTH, required=False)
    image_one = forms.ImageField(required=False)
    image_two = forms.ImageField(required=False)
    remove_image_one = forms.CharField(max_length=10, required=False)
    remove_image_two = forms.CharField(max_length=10, required=False)
    button_one_label = forms.CharField(max_length=MAX_BUTTON_LABEL_LENGTH)
    button_two_label = forms.CharField(max_length=MAX_BUTTON_LABEL_LENGTH)
    tags = forms.CharField(max_length=MAX_TAGS_LENGTH)


class TagSearch(forms.Form):
    tag = forms.CharField(max_length=MAX_TAG_LENGTH)


class VoteOption(forms.Form):
    vote_option = forms.ChoiceField(choices=(
        ('1', '1'), ('2', '2')
    ))


class Comment(forms.Form):
    comment = forms.CharField(max_length=MAX_COMMENT_LENGTH)


class CommentVote(forms.Form):
    vote_option = forms.ChoiceField(choices=(
        ('Up', 'Up'), ('Down', 'Down')
    ))


class DeleteComment(forms.Form):
    delete_comment = forms.BooleanField()


class Sort(forms.Form):
    sort_type = None

    choices=[
        ('votes-True', 'votes-True'),
        ('votes-False', 'votes-False'),
        ('date_posted-True', 'date_posted-True'),
        ('date_posted-False', 'date_posted-False'),
        ('comments-True', 'comments-True'),
        ('comments-False', 'comments-False')
    ]

    def set_sort_type(self, sort_type):
        self.sort_type = sort_type


    sort_option = forms.ChoiceField(choices=choices)

class Page(forms.Form):
    page = forms.CharField(max_length=3)


class ModifyPost(forms.Form):
    option = forms.ChoiceField(choices=(
        ('Delete', 'Delete'), ('Edit', 'Edit')
    ))