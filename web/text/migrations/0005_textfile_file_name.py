# Generated by Django 2.2.1 on 2019-06-13 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('text', '0004_auto_20190613_1436'),
    ]

    operations = [
        migrations.AddField(
            model_name='textfile',
            name='file_name',
            field=models.CharField(default='', max_length=255),
        ),
    ]
