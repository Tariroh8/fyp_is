# Generated by Django 5.0.1 on 2024-04-30 19:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0024_auto_20240430_2025'),
    ]

    operations = [
        migrations.AddField(
            model_name='case',
            name='ward',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.ward'),
        ),
    ]
