from django.shortcuts import render, get_object_or_404
from .models import Category #Categoryモデルをインポート

#カテゴリ詳細ビュー
def category_detail(request, category_slug):
    #ここにカテゴリ詳細を取得して表示するロジックを記述します
    #例: category = get_object_or_404(Category, slug=category_slug)
    return render(request, 'categories/category_detail.html', {'category_slug': category_slug})

#もしcategories/urls.pyでカテゴリ一覧を表示するパスを定義している場合
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'categories/category_list.html', {'categories': categories})