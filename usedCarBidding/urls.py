from django.urls import path
from . import views
from .views import chat, respond

urlpatterns = [
    path("dbconnection/", views.check_db_connection, name="check_db_connection"),
    path('', views.testmysql),
    path('respond/', respond, name='respond'),
]
