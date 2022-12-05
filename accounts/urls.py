from django.contrib import admin
from django.urls import path
from .views import * # viewsteki tüm fonklar eklendi

urlpatterns =[
    path('', home , name="home"), #home fonk için viewse gidiyorum
    path('register', register_attempt, name="register_attempt"),
    path('login', login_attempt, name="login_attempt"),
    path('token', token_send, name="token_send"),
    path('success', success, name="success"),
    path('verify/<auth_token>', verify, name="verify"),
    path('error', error_page, name="error")
]