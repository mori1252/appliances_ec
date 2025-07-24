from django.urls import path, include
from . import views

app_name = 'products'

urlpatterns = [
    #商品一覧ページ
    path('', views.product_list, name='list'),

    #商品詳細ページ
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),

    #商品登録・編集（共通）
    path('product/<str:action>/', views.product_form, name='product_form'),

    #商品編集のみのURL（必要に応じて）
    path('product/<str:action>/<int:pk>/', views.product_form, name='product_form_edit'),
    
    path('admin/', include('products.admin_urls')),
]