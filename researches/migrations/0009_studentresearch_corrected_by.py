# Generated by Django 3.0.5 on 2020-05-27 19:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('researches', '0008_auto_20200505_2209'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentresearch',
            name='corrected_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
