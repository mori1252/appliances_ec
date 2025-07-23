from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='list'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
#     path('category/<slug:category_slug>/', views.product_list_by_category, name='list_by_category'),
]