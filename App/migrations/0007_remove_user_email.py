# Generated by Django 4.2.2 on 2023-06-13 10:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0006_alter_post_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='email',
        ),
    ]
