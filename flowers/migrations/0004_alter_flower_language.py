# Generated by Django 5.1.7 on 2025-03-27 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flowers', '0003_flower_language'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flower',
            name='language',
            field=models.CharField(choices=[('en', 'English'), ('uk', 'Ukrainian')], default='en', max_length=2),
        ),
    ]
