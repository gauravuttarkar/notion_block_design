from django.http import HttpResponse, JsonResponse
from home.models import Row, Column, Table, Data
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
import json

def index(request):
    return HttpResponse("Hello, world. You're at the home index.")

@csrf_exempt
def addColumn(request, table_id):
    if request.method == "POST":
        data = json.loads( request.body )
        column_name = data["column_name"]
        column_type = data["column_type"]
        default_value = data["default_value"]
        column_details = getMaxColumnIdandColumnOrder(table_id)
        new_column = Column(column_name = column_name, column_type = column_type,
                            column_order = column_details["max_column_order"]+1,
                            column_id= column_details["max_column_id"]+1, table_id=table_id);
        new_column.save()
        all_rows = Row.objects.filter(table_id=table_id)
        for row in all_rows:
            new_data = Data(row_id=row.row_id, column_id=new_column.column_id, value=default_value, table_id=table_id)
            new_data.save()
        return HttpResponse("POST request succeeded")
    else:
        return HttpResponse("Should be a POST request")

@csrf_exempt
def deleteColumn(request, table_id, column_id):
    if request.method == "DELETE":
        column = Column.objects.get(table_id=table_id, column_id = column_id )
        column.delete()
        return HttpResponse("Delete request succeeded")
    else:
        return HttpResponse("Request method not delete")
@csrf_exempt
def reorderColumn(request, table_id, column_id, new_order):
    max_column = getMaxColumnIdandColumnOrder(table_id)
    if(new_order > max_column["max_column_order"]):
        return HttpResponse("Column reorder failed. Order greater than number of columns")

    column_to_be_changed = Column.objects.get(table_id=table_id, column_id=column_id)
    old_column_to_be_changed = Column.objects.get(table_id=table_id, column_order=new_order)
    old_order = column_to_be_changed.column_order
    old_column_to_be_changed.column_order = old_order
    column_to_be_changed.column_order = new_order
    with transaction.atomic():
        old_column_to_be_changed.save()
        column_to_be_changed.save()
    return HttpResponse("Column reorder successful")
@csrf_exempt
def editData(request, table_id, column_id, row_id, new_value):
    data = Data.objects.get(table_id=table_id, row_id=row_id, column_id = column_id)
    data.value = new_value
    data.save()
    return HttpResponse("Data successfully updated")

@csrf_exempt
def addRow(request, table_id ):
    if request.method == "POST":
        row_details = getMaxRowIdandRowOrder(table_id)
        new_row = Row(table_id=table_id, row_id = row_details["max_row_id"] + 1,
                      row_order = row_details["max_row_order"] + 1)
        new_row.save()
        data = json.loads( request.body )
        all_columns = Column.objects.filter(table_id=table_id)
        for column in all_columns:
            new_data = Data(table_id=table_id, row_id=new_row.row_id, column_id=column.column_id, value= data[column.column_name] )
            new_data.save()

        return HttpResponse("POST request succeeded")
    else:
        return HttpResponse("Should be a POST request")
@csrf_exempt
def deleteRow(request, table_id, row_id):
    if request.method == "DELETE":
        row = Row.objects.get(table_id=table_id, row_id = row_id )
        row.delete()
        return HttpResponse("Delete request succeeded")
    else:
        return HttpResponse("Request method not delete")
@csrf_exempt
def reorderRow(request, table_id, row_id, new_order):
    max_row = getMaxRowIdandRowOrder(table_id)
    if (new_order > max_row["max_row_order"]):
        return HttpResponse("Row reorder failed. Order greater than number of rows")
    row_to_be_changed = Row.objects.get(table_id=table_id, row_id=row_id)
    old_row_to_be_changed = Row.objects.get(table_id=table_id, row_order=new_order)
    old_order = row_to_be_changed.row_order
    old_row_to_be_changed.row_order = old_order
    row_to_be_changed.row_order = new_order
    old_row_to_be_changed.save()
    row_to_be_changed.save()
    return HttpResponse("Row reorder successful")

@csrf_exempt
def getRows(request, table_id):
    all_rows = Row.objects.filter(table_id=table_id).order_by("row_order")
    all_columns = Column.objects.filter(table_id=table_id).order_by("column_order")
    table_details = Table.objects.get(table_id=table_id)
    data_dict = {
        'table_id': table_id,
        'table_name': table_details.table_name,
        'rows': []
    }
    for row in all_rows:
        new_row = {}
        for column in all_columns:
            data_details = Data.objects.get(table_id=table_id, row_id=row.row_id, column_id=column.column_id)
            new_row[ column.column_name ] = data_details.value
            new_row[ "row_id" ] = row.row_id
        data_dict["rows"].append(new_row)

    return JsonResponse(data_dict)

def getMaxRowIdandRowOrder(table_id):
    max_row_order = Row.objects.filter(table_id=table_id).order_by("-row_order")[0]
    max_row_id = Row.objects.filter(table_id=table_id).order_by("-row_id")[0]
    return {"max_row_order" : max_row_order.row_order, "max_row_id": max_row_id.row_id }

def getMaxColumnIdandColumnOrder(table_id):
    max_column_order = Column.objects.filter(table_id=table_id).order_by("-column_order")[0]
    max_column_id = Column.objects.filter(table_id=table_id).order_by("-column_id")[0]
    return {"max_column_order" : max_column_order.column_order, "max_column_id": max_column_id.column_id }