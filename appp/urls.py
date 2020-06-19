from django.urls import path,re_path
from .views  import index,create_product,register,detail_product,profile,buy_listt,delete_buy_listt
from django.contrib.auth.views import LoginView,LogoutView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[
    path("",index,name="index"),
    path("new/",create_product,name="product-create"),
    re_path(r"product/(?P<slug>[-\w]+)",detail_product,name="product-detail"),
    path("buy-list/",buy_listt,name="buy-list"),
    re_path(r"delete-buy-list/(?P<slug>[-\w]+)",delete_buy_listt,name="delete-buy-list"),
    path("register/",register,name="register"),
    path("login/",LoginView.as_view(template_name="appp/login.html"),name="login"),
    path("logout/",LogoutView.as_view(template_name="appp/logout.html"),name="logout"),
    path("profile/",profile,name="profile"),
]

