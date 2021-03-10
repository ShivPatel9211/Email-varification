from django.urls import path 
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login_attemp, name='login'),
    path('register', views.register_attemp, name='register'),
    path('token', views.token_send, name='token'),
    path('success', views.success, name='success'),
    path('verify/<token>', views.verify, name='verify'),
    path('error', views.error, name='error'),
  
]