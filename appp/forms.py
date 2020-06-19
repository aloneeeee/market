from django import forms
from .models import Product,Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class NewProduct(forms.ModelForm):
    class Meta:
        model=Product
        fields=["name","detail","category","price","slug","image"]


class RegisterForm(UserCreationForm):
    username=forms.CharField(label="نام کاربری")
    email=forms.EmailField(label="ایمیل")
    password1=forms.CharField(label="پسورد")
    password2=forms.CharField(label="پسورد")

    
    class Meta:
        model=User
        fields=["username","email","password1","password2"]
