# Generated by Django 4.0.3 on 2025-06-10 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_cliopatria_polity_end_year_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Leaderboard',
            fields=[
                ('initials', models.CharField(max_length=3, primary_key=True, serialize=False, unique=True)),
                ('score', models.IntegerField(default=0)),
            ],
        ),
    ]
