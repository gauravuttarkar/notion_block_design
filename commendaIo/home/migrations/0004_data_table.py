# Generated by Django 4.2.1 on 2023-05-28 08:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_rename_column_data_column'),
    ]

    operations = [
        migrations.AddField(
            model_name='data',
            name='table',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='home.table'),
        ),
    ]
