from django.shortcuts import render, get_object_or_404
from .models import Product
from categories.models import Category

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    #商品一覧を取得するロジック
    products = Product.objects.all()
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    return render(request, 'products/product_list.html', {
        'category': category,
        'categories': categories,
        'products': products
    })

def product_detail(request, id, slug):
    #特定の商品詳細を取得するロジック
    product = get_object_or_404(Product, id=id, slug=slug)
    return render(request, 'products/product_detail.html', {'product': product})
