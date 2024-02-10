# Generated by Django 5.0.1 on 2024-02-09 23:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_remove_habit_completed_remove_habit_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='habit',
            name='difficulty',
            field=models.CharField(choices=[('TR', 'Trivial'), ('EA', 'Easy'), ('ME', 'Medium'), ('HA', 'Hard')], default='ME', max_length=2),
        ),
    ]