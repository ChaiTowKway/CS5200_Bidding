from django.urls import path
from . import views
from .views import chat, respond, register
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path("dbconnection/", views.check_db_connection, name="check_db_connection"),
    path('', views.car_list, name='home'),
    path('', views.testmysql),
    path('respond/', respond, name='respond'),
    path('detail/', views.car_detail),
    path('detailSeller/', views.car_detail_seller),
    path('bidding/', views.place_bid),
    path('endBidding/', views.end_bidding_for_seller),
    path('comments/', views.get_comments_for_auction),
    path('creatComment/', views.createComment),
    path('replyComment/', views.createReply),
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(template_name='registration/login.html'),
         name='login_url'),
    path('logout/', LogoutView.as_view(next_page='home'),
         name='logout'),  # Redirect to 'home' after logout

]
