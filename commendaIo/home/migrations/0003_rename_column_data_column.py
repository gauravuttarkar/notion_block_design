# Generated by Django 4.2.1 on 2023-05-28 07:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_column_data_row_table_delete_govtid_delete_user_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='data',
            old_name='Column',
            new_name='column',
        ),
    ]
