# Generated by Django 3.0.5 on 2020-05-04 00:18

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('researches', '0006_auto_20200425_1608'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentresearch',
            name='student',
        ),
        migrations.AddField(
            model_name='studentresearch',
            name='students',
            field=models.ManyToManyField(related_name='student_researches', to=settings.AUTH_USER_MODEL),
        ),
    ]