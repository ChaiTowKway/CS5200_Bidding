from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("dbconnection/", views.check_db_connection, name="check_db_connection"),
]
