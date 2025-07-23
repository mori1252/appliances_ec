from django.db import models

class Product(models.Model):
    #Categoryを文字列で参照する('アプリ名.モデル名')
    category = models.ForeignKey('categories.Category', related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name'] #名前でソートする

