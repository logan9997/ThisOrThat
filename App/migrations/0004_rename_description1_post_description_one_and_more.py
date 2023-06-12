# Generated by Django 4.2.2 on 2023-06-12 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0003_alter_post_image1_alter_post_image2'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='description1',
            new_name='description_one',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='description2',
            new_name='description_two',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='image1',
            new_name='image_one',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='image2',
            new_name='image_two',
        ),
        migrations.AlterField(
            model_name='post',
            name='date_posted',
            field=models.DateField(auto_now_add=True),
        ),
    ]
