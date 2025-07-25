from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.conf import settings

class CustomUserManager(BaseUserManager):
    def create_user(self, username, mail_address, password=None):
        if not username or not mail_address:
            raise ValueError('ユーザー名とメールアドレスは必須です')
        user = self.model(username=username, mail_address=mail_address)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, mail_address, password):
        user = self.create_user(username=username, mail_address=mail_address, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    
class CustomUser(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    mail_address = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['mail_address']

    def __str__(self):
        return self.username
    
class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='addresses')
    postal_code = models.CharField(max_length=10)
    prefecture = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=255, blank=True, null=True)
    building = models.CharField(max_length=255, blank=True, null=True)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.prefecture} {self.city} {self.street} {self.building or ""} ({self.postal_code})'