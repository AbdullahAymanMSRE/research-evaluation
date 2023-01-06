# Generated by Django 2.2.12 on 2020-06-01 00:54

from django.db import migrations, models
import researches.models


class Migration(migrations.Migration):

    dependencies = [
        ('researches', '0009_studentresearch_corrected_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentresearch',
            name='research_file',
            field=models.FileField(upload_to='', validators=[researches.models.validate_file_extension]),
        ),
    ]
