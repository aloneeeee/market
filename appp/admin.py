from django.contrib import admin
from .models import Product,Comment,UserList

# Register your models here.
admin.site.register(Product)
admin.site.register(Comment)
admin.site.register(UserList)