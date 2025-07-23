from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        ordering = ('name',) #カテゴリを名前順にソート（任意）

    def __str__(self):
        return self.name
    
    # 必要に応じて、URLを取得するメソッドを追加することもできます
    # from django.urls import reverse
    # def get_absolute_url(self):
    #    return reverse('products:list_by_category', args=[self.slug])