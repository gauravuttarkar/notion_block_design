from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:table_id>/", views.getRows, name="getRows"),
    path("<int:table_id>/addColumn", views.addColumn, name="addColumn"),
    path("<int:table_id>/deleteColumn/<int:column_id>", views.deleteColumn, name="deleteColumn"),
    path("<int:table_id>/reorderColumn/<int:column_id>/<int:new_order>", views.reorderColumn, name="reorderColumn"),
    path("<int:table_id>/addRow", views.addRow, name="addRow"),
    path("<int:table_id>/deleteRow/<int:row_id>", views.deleteRow, name="deleteRow"),
    path("<int:table_id>/reorderRow/<int:row_id>/<int:new_order>", views.reorderRow, name="reorderRow"),
    path("<int:table_id>/editData/<int:row_id>/<int:column_id>/<str:new_value>", views.editData, name="editData"),
]