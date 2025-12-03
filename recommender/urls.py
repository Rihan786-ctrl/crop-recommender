
from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup_view, name='signup'),
    path('predict/', predict_view, name='predict'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('history/', history_view, name='history'),
    path('profile/', profile_view, name='profile'),
    path('history_delete/<int:id>/', user_delete_prediction_view, name='user_delete_prediction'),
    path('admin_login/', admin_login_view, name='admin_login'),
    path('admin_dashboard/', admin_dashboard_view, name='admin_dashboard'),
    path('admin_users_view/', admin_users_view, name='admin_users_view'),
    path('admin_user_delete/<int:id>/', admin_user_delete_view, name='admin_user_delete'),
    path('admin_logout_view/', admin_logout_view, name='admin_logout_view'),
    path('admin_view_prediction/', admin_view_prediction, name='admin_view_prediction'),
]