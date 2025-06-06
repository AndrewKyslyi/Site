# Generated by Django 5.1.7 on 2025-03-27 22:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flowers', '0004_alter_flower_language'),
    ]

    operations = [
        migrations.AddField(
            model_name='flower',
            name='description_uk',
            field=models.TextField(blank=True, null=True, verbose_name='Ukrainian Description'),
        ),
        migrations.AddField(
            model_name='flower',
            name='is_featured',
            field=models.BooleanField(default=False, verbose_name='Featured on Homepage'),
        ),
    ]
