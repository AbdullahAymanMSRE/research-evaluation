# Generated by Django 3.0.5 on 2020-04-21 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('researches', '0002_studentresearch_seen'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentresearch',
            name='corrected',
            field=models.BooleanField(default=False),
        ),
    ]