from django.urls import path
from . import views

urlpatterns = [
    path("dbconnection/", views.check_db_connection, name="check_db_connection"),
    path('', views.testmysql),
]
