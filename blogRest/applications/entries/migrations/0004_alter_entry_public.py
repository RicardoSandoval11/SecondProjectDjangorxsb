# Generated by Django 4.1.7 on 2023-03-30 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entries', '0003_alter_entry_public'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='public',
            field=models.BooleanField(),
        ),
    ]
