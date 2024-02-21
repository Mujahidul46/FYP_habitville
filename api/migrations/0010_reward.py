# Generated by Django 5.0.1 on 2024-02-14 14:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_alter_user_life_points'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reward',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('notes', models.TextField(blank=True, null=True)),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rewards', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]