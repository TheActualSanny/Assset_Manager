# Generated by Django 5.2 on 2025-05-01 13:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Agency',
            fields=[
                ('model_name', models.CharField(max_length=50, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('project_name', models.CharField(max_length=70, primary_key=True, serialize=False)),
                ('associated_agency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manager.agency')),
            ],
        ),
    ]
