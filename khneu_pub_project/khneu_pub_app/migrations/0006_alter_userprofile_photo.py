# Generated by Django 4.2.7 on 2023-11-21 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('khneu_pub_app', '0005_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='photo',
            field=models.ImageField(default='images/profile_photo/default_photo.png', upload_to='images/profile_photo'),
        ),
    ]