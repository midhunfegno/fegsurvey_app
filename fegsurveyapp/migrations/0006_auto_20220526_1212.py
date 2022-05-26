# Generated by Django 3.2.13 on 2022-05-26 12:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fegsurveyapp', '0005_auto_20220525_0636'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='surveyentry',
            name='answers',
        ),
        migrations.AddField(
            model_name='surveyentry',
            name='is_complete',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='surveyentry',
            name='survey',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='fegsurveyapp.survey'),
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answers', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='fegsurveyapp.answers')),
                ('surveyentry', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='fegsurveyapp.surveyentry')),
            ],
        ),
    ]