# Generated by Django 4.2.7 on 2023-11-21 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('khneu_pub_app', '0008_alter_userprofile_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='photo',
            field=models.ImageField(default='images/profile_photo/default_photo.png', upload_to='images/profile_photo'),
        ),
    ]
