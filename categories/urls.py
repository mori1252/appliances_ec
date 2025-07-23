from django.urls import path
from . import views

app_name = 'categories'

urlpatterns = [
    path('<slug:category_slug>/', views.category_detail, name='detail'),
]