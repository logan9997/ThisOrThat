from django.db import models
from .config import (
    USERNAME_LENGTH, EMAIL_LENGTH, PASSWORD_LENGTH,
    TITLE_LENGTH, DESCRIPTION_LENGTH, STATUS_LENGTH,
    TAGS_LENGTH, OPTION_LENGTH
)


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=USERNAME_LENGTH)
    email = models.EmailField(max_length=EMAIL_LENGTH)
    password = models.CharField(max_length=PASSWORD_LENGTH)


class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=TITLE_LENGTH)
    description_one = models.CharField(max_length=DESCRIPTION_LENGTH)
    description_two = models.CharField(max_length=DESCRIPTION_LENGTH)
    image_one = models.ImageField(null=True, blank=True, upload_to='images/')
    image_two = models.ImageField(null=True, blank=True, upload_to='images/')
    status = models.CharField(max_length=STATUS_LENGTH, default='Open', choices=(
        ('Open', 'Open'), ('Closed', 'Closed')
    ))
    date_posted = models.DateField(auto_now_add=True)
    tags = models.CharField(max_length=TAGS_LENGTH)


class Vote(models.Model):
    vote_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    option = models.CharField(max_length=OPTION_LENGTH, choices=(
        ('1', '1'), ('2', '2')
    ))

