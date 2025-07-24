from django.db import models
from django.utils.text import slugify
import unicodedata

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        # slug が空なら name から生成
        if not self.slug:
            normalized_name = unicodedata.normalize('NFKC', self.name)
            self.slug = slugify(normalized_name)
        super().save(*args, **kwargs)


    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        ordering = ('name',) #カテゴリを名前順にソート（任意）

    def __str__(self):
        return self.name