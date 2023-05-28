# Generated by Django 4.2.1 on 2023-05-28 07:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Column',
            fields=[
                ('column_id', models.IntegerField(primary_key=True, serialize=False)),
                ('column_name', models.CharField(max_length=64)),
                ('column_type', models.CharField(max_length=32)),
                ('column_order', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Data',
            fields=[
                ('data_id', models.IntegerField(primary_key=True, serialize=False)),
                ('value', models.CharField(max_length=256)),
                ('Column', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.column')),
            ],
        ),
        migrations.CreateModel(
            name='Row',
            fields=[
                ('row_id', models.IntegerField(primary_key=True, serialize=False)),
                ('row_order', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('table_id', models.IntegerField(primary_key=True, serialize=False)),
                ('table_name', models.CharField(max_length=256)),
            ],
        ),
        migrations.DeleteModel(
            name='GovtId',
        ),
        migrations.DeleteModel(
            name='User',
        ),
        migrations.AddField(
            model_name='row',
            name='table',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.table'),
        ),
        migrations.AddField(
            model_name='data',
            name='row',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.row'),
        ),
        migrations.AddField(
            model_name='column',
            name='table',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.table'),
        ),
    ]
