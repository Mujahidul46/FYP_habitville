# Generated by Django 5.0.1 on 2024-03-28 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_category_habit_categories'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='main_content_color',
            field=models.CharField(default='#e4e4e4', max_length=7),
        ),
        migrations.AddField(
            model_name='user',
            name='navbar_color',
            field=models.CharField(default='#8e8e8e', max_length=7),
        ),
    ]
