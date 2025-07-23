from django.contrib import admin
from django.urls import path, include
from products import views as product_views

urlpatterns = [
    path('admin/', admin.site.urls),
    #トップページ
    path('', product_views.product_list, name='home'),

    #各アプリケーションのURLconfを含める
    path('users/', include('users.urls')),
    path('products/', include('products.urls')),
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),
    path('categories/', include('categories.urls')),
]
