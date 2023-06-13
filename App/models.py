from django.db import models
from .config import (
    MAX_USERNAME_LENGTH, MAX_PASSWORD_LENGTH,
    MAX_TITLE_LENGTH, MAX_DESCRIPTION_LENGTH, MAX_STATUS_LENGTH,
    MAX_TAGS_LENGTH, MAX_OPTION_LENGTH
)


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=MAX_USERNAME_LENGTH)
    password = models.CharField(max_length=MAX_PASSWORD_LENGTH)


class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=MAX_TITLE_LENGTH)
    description_one = models.CharField(max_length=MAX_DESCRIPTION_LENGTH)
    description_two = models.CharField(max_length=MAX_DESCRIPTION_LENGTH)
    image_one = models.ImageField(null=True, blank=True, upload_to='images/')
    image_two = models.ImageField(null=True, blank=True, upload_to='images/')
    status = models.CharField(max_length=MAX_STATUS_LENGTH, default='Open', choices=(
        ('Open', 'Open'), ('Closed', 'Closed')
    ))
    date_posted = models.DateField(auto_now_add=True)
    tags = models.CharField(max_length=MAX_TAGS_LENGTH)


class Vote(models.Model):
    vote_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    option = models.CharField(max_length=MAX_OPTION_LENGTH, choices=(
        ('1', '1'), ('2', '2')
    ))
