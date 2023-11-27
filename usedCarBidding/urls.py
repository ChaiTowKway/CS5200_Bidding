from django.urls import path
from . import views

urlpatterns = [
    path("dbconnection/", views.check_db_connection, name="check_db_connection"),
    path('', views.testmysql),
    path('detail/', views.car_detail),
    path('detailSeller/', views.car_detail_seller),
    path('bidding/', views.place_bid),
    path('endBidding/', views.end_bidding_for_seller),
]
