# Generated by Django 3.0.5 on 2020-04-20 22:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('unistruct', '0003_auto_20200420_2247'),
        ('users', '0003_auto_20200419_1941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='faculty',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to='unistruct.Faculty'),
        ),
        migrations.AlterField(
            model_name='user',
            name='subjects',
            field=models.ManyToManyField(related_name='users', to='unistruct.Subject'),
        ),
    ]
