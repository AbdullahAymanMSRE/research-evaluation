# Generated by Django 3.0.5 on 2020-05-14 10:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('unistruct', '0008_remove_team_sdone'),
        ('users', '0012_auto_20200508_1245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='control_head',
            field=models.BooleanField(default=False, verbose_name='Control Head'),
        ),
        migrations.AlterField(
            model_name='user',
            name='dprtmngr',
            field=models.BooleanField(default=False, verbose_name='Department Head'),
        ),
        migrations.AlterField(
            model_name='user',
            name='team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='unistruct.Team', verbose_name='Group'),
        ),
    ]
