# Generated by Django 4.2.7 on 2023-11-18 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('khneu_pub_app', '0003_alter_article_upload_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='first_name',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='last_name',
            field=models.CharField(default='', max_length=30),
        ),
    ]