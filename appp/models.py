from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.shortcuts import reverse

from PIL import Image


class Product(models.Model):
    name=models.CharField(max_length=20)
    detail=models.TextField(max_length=1500)
    image=models.ImageField(upload_to="product_image")
    category=models.CharField(max_length=20)
    price=models.IntegerField(default=0)
    slug=models.SlugField(null=True,blank=True,allow_unicode=True)
    date_created=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    #def get_absolute_url(self):
    #    return reverse('product-detail', kwargs={'slug': self.slug})
    
    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)

        img=Image.open(self.image.path)

        if img.height > 600 or img.width >600:
            output_size=(600,600)
            img.thumbnail(output_size)
            img.save(self.image.path)



class Comment(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='comments')
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    class Meta:
        ordering=("-created_on",)
    def __str__(self):
        return f"comment by {self.user} on {self.created_on}"


class UserList(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='products')
    saved=models.BooleanField(default=False)
    buy=models.BooleanField(default=False)
    buy_num=models.PositiveSmallIntegerField(default=1)
    def __str__(self):
        return f"{self.user} and {self.product}" 

