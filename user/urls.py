from django.urls import path
from user.views import *
urlpatterns = [
    path('login/',UserLoginView.as_view(),name = 'login'),
    path('register/',RegisterView.as_view(),name = 'register'),
    path('account/',AccountView.as_view(),name = 'account'),
    path('logout/',UserLogoutView.as_view(),name = 'logout')
]