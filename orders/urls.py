from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='create'),
    path('complete/<int:order_id>/', views.order_complete, name='complete'),
    path('history/', views.order_history, name='history'),
    path('<int:order_id>/', views.order_detail, name='detail'),
]