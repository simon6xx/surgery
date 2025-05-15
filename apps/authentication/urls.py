from django.urls import path

from .views import *

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('user-info', UserInfoView.as_view(), name='user-info'),
    path('users', UserListView.as_view(), name='users'),
]
