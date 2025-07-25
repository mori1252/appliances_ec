from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Product
from categories.models import Category
from .forms import ProductForm
from django.urls import reverse

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

def is_admin(user):
    return user.is_staff

# 商品一覧・検索ページ(管理者用ダッシュボード)
@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    search_query = request.GET.get('search', '')
    if search_query:
        products = Product.objects.filter(name__icontains=search_query)
    else:
        products = Product.objects.all()

    return render(request, 'products/admin_dashboard.html', {
        'products': products, 'search_query': search_query
    })

# 商品登録・編集の共通ビュー
@login_required
@user_passes_test(is_admin)
def product_form(request, action, pk=None):
    if action not in ('add', 'edit'):
        return redirect('admin_dashboard')
    
    if action == 'add':
        product = None
        title = '商品登録'
    else:
        product = get_object_or_404(Product, pk=pk)
        title = '商品編集'

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
        
    else:
        form = ProductForm(instance=product)

    return render(request, 'products/product_form.html', {'form': form, 'title': title})