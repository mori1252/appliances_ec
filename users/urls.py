from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.user_register, name='register'),
    path('mypage/', views.user_mypage, name='mypage'),
    path('mypage/address/delete/<int:address_id>/', views.delete_address, name='delete_address'),
]