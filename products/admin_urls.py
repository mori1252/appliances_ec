from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('add/', views.product_form, {'action': 'add'}, name='product_add'), #新規登録
    path('<int:pk>/edit/', views.product_form, {'action': 'edit'}, name='product_edit'), #編集
]