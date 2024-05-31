# Generated by Django 5.0.1 on 2024-04-09 16:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_alter_case_farmer1_delete_farmer'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Farmer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=254, null=True)),
                ('file', models.CharField(max_length=75, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('district', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.district')),
                ('species_owned', models.ManyToManyField(blank=True, to='backend.spece')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('ward', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.ward')),
            ],
        ),
        migrations.AlterField(
            model_name='case',
            name='farmer1',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.farmer'),
        ),
    ]
