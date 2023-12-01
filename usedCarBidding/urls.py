from django.urls import path
from . import views
from .views import chat, respond, register
from django.contrib.auth.views import LoginView


urlpatterns = [
    path("dbconnection/", views.check_db_connection, name="check_db_connection"),
    path('', views.testmysql, name='home'),
    path('respond/', respond, name='respond'),
]
