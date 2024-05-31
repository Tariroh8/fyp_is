# Generated by Django 5.0.1 on 2024-04-29 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0016_vet_officer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ward',
            old_name='district1',
            new_name='district_foreign',
        ),
        migrations.RemoveField(
            model_name='vet_officer',
            name='species_owned',
        ),
        migrations.RemoveField(
            model_name='ward',
            name='case_recor',
        ),
        migrations.RemoveField(
            model_name='ward',
            name='hotspot',
        ),
        migrations.RemoveField(
            model_name='ward',
            name='num_of_cas',
        ),
        migrations.AlterField(
            model_name='vet_officer',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
