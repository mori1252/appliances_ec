from django.db import models
from django.urls import reverse #商品詳細ページのURLを取得するために追加

class Product(models.Model):
    #Categoryを文字列で参照する('アプリ名.モデル名')
    category = models.ForeignKey('categories.Category', related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ('name',) #名前でソートする
        indexes = [
            models.Index(fields=['id', 'slug']),
        ]

    #個々の商品詳細ページへのURLを返す
    #products:product_detailはproducts/urls.pyで定義
    def get_absolute_url(self):
        return reverse('products:product_detail', args=[self.id, self.slug])

