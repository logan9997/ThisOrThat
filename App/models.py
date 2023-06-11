from django.db import models

#USER
USERNAME_LENGTH = 16
EMAIL_LENGTH = 60
PASSWORD_LENGTH = 24

#POST
DESCRIPTION_LENGTH = 500
TAGS_LENGTH = 120
STATUS_LENGTH = 6

#VOTE
OPTION_LENGTH = 1

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=USERNAME_LENGTH)
    email = models.EmailField(max_length=EMAIL_LENGTH)
    password = models.CharField(max_length=PASSWORD_LENGTH)


class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description1 = models.CharField(max_length=DESCRIPTION_LENGTH)
    description2 = models.CharField(max_length=DESCRIPTION_LENGTH)
    image1 = models.ImageField()
    image2 = models.ImageField()
    status = models.CharField(max_length=STATUS_LENGTH, choices=(
        ('Open', 'Open'), ('Closed', 'Closed')
    ))
    date_posted = models.DateField()
    tags = models.CharField(max_length=TAGS_LENGTH)


class Vote(models.Model):
    vote_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    option = models.CharField(max_length=OPTION_LENGTH, choices=(
        ('1', '1'), ('2', '2')
    ))

