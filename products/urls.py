from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='list'),
    path('<int:product_id>/', views.product_detail, name='detail'),
#     path('category/<slug:category_slug>/', views.product_list_by_category, name='list_by_category'),
]