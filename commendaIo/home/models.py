from django.db import models

class Table(models.Model):
    table_id = models.IntegerField(primary_key=True)
    table_name = models.CharField(max_length=256)

class Column(models.Model):
    column_id = models.IntegerField(primary_key=True)
    column_name = models.CharField(max_length=64)
    column_type = models.CharField(max_length=32)
    column_order = models.IntegerField()
    table = models.ForeignKey(Table, on_delete=models.CASCADE)

class Row(models.Model):
    row_id = models.IntegerField(primary_key=True)
    row_order = models.IntegerField()
    table = models.ForeignKey(Table, on_delete=models.CASCADE)

class Data(models.Model):
    data_id = models.IntegerField(primary_key=True)
    row = models.ForeignKey(Row, on_delete=models.CASCADE)
    column = models.ForeignKey(Column, on_delete=models.CASCADE)
    value = models.CharField(max_length=256)
    table = models.ForeignKey(Table, on_delete=models.CASCADE, default=1)