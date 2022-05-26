# Generated by Django 3.2.13 on 2022-05-25 05:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fegsurveyapp', '0002_answers_text'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answers',
            name='question',
        ),
        migrations.AddField(
            model_name='answers',
            name='question',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='fegsurveyapp.question'),
        ),
    ]
