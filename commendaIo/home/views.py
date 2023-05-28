from django.http import HttpResponse, JsonResponse
from home.models import Row, Column, Table, Data
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return HttpResponse("Hello, world. You're at the home index.")

@csrf_exempt
def addColumn(request, table_id):
    if request.method == "POST":
        data = request.POST
        column_name = data.get("column_name")
        column_type = data.get("column_type")
        column_order = data.get("column_order")
        default_value = data.get("default_value")
        new_column = Column(column_name = column_name, column_type = column_type, column_order = column_order);
        new_column.save()
        all_rows = Row.objects.filter(table_id=table_id)
        for row in all_rows:
            new_data = Data(row_id=row.row_id, column_id=new_column.column_id, value=default_value, table_id=table_id)
            new_data.save()
        return HttpResponse("POST request succeeded")
    else:
        return HttpResponse("Should be a POST request")

def deleteColumn(request, table_id, column_id):
    column = Column.objects.get(table_id=table_id, row_id = column_id )
    column.delete()
    return HttpResponse("Delete request succeeded")

def reorderColumn(request, table_id, column_id, new_order):
    column_to_be_changed = Column.objects.get(table_id=table_id, column_id=column_id)
    old_column_to_be_changed = Column.objects.get(table_id=table_id, column_order=new_order)
    old_order = column_to_be_changed.column_order
    old_column_to_be_changed.column_order = old_order
    column_to_be_changed.column_order = new_order
    old_column_to_be_changed.save()
    column_to_be_changed.save()
    return HttpResponse("Column reorder successful")

def editData(request, table_id, column_id, row_id, new_value):
    data = Data.objects.get(table_id=table_id, row_id=row_id, column_id = column_id)
    data.value = new_value
    data.save()
    return HttpResponse("Data successfully updated")

def addRow(request, table_id ):
    if request.method == "POST":
        new_row = Row(table_id=table_id)
        data = request.POST
        all_columns = Column.objects.filter(table_id=table_id)
        for column in all_columns:
            new_data = Data(table_id=table_id, row_id=new_row.row_id, column_id=column.column_id, value=data.get(column.column_name))
            new_data.save()
        new_row.save()
        return HttpResponse("POST request succeeded")
    else:
        return HttpResponse("Should be a POST request")

def deleteRow(request, table_id, row_id):
    row = Row.objects.get(table_id=table_id, row_id = row_id )
    row.delete()
    return HttpResponse("Delete request succeeded")

def reorderRow(request, table_id, row_id, new_order):
    row_to_be_changed = Row.objects.get(table_id=table_id, row_id=row_id)
    old_row_to_be_changed = Row.objects.get(table_id=table_id, row_order=new_order)

    old_order = row_to_be_changed.row_order

    old_row_to_be_changed.row_order = old_order
    row_to_be_changed.row_order = new_order

    old_row_to_be_changed.save()
    row_to_be_changed.save()

    return HttpResponse("Row reorder successful")

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
        data_dict['rows'].append(new_row)

    return JsonResponse(data_dict)

