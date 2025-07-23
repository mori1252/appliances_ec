from django.shortcuts import render, get_object_or_404
from .models import Product
from categories.models import Category

def product_list(request):
    #商品一覧を取得するロジック
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})

def product_detail(request, product_id):
    #特定の商品詳細を取得するロジック
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'products/product_detail.html', {'product': product})

def product_list_by_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    return render(request, 'products/product_list.html', {'products': products, 'category': category})