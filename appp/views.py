from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.views.generic import ListView
from django.contrib import messages


from .models import Product,Comment,UserList
from .forms import NewProduct,RegisterForm


def index(request):
    products=Product.objects.all()
    if request.user.is_authenticated :
        product=UserList.objects.filter(user=request.user,buy=True)
        return render(request,"appp/index.html",{"products":products,"count":len(product)})
    return render(request,"appp/index.html",{"products":products})

@user_passes_test(lambda u: u.is_superuser)
def create_product(request):
    if request.method=="POST":
        form=NewProduct(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect("index")
        else:
            print("not valid")
    else:        
        form=NewProduct()
    con={
        "form":form
    }
    return render(request,"appp/new_product.html",con)


def detail_product(request,slug):

    product=Product.objects.filter(slug=slug)
    
    if not request.user.is_anonymous:
    
        comment=Comment.objects.filter(product=product[0],user=request.user,active=True)
        p_count=UserList.objects.filter(user=request.user,buy=True)
        is_save=UserList.objects.filter(user=request.user,product=product[0],saved=True)
        is_buy=UserList.objects.filter(user=request.user,product=product[0],buy=True)
        
        if len(is_save) ==0:
            empty_save=True
        else:
            empty_save=False



        if len(is_buy) ==0:
            empty_buy=True
        else:
            empty_buy=False



        if len(comment) == 0:
            empty_comment=True
        else:
            empty_comment=False

        if request.method=="POST":
            print(request.POST)

            if "body" in request.POST:
                if request.POST["body"] !="":
                    Comment.objects.create(product=product[0],user=request.user,body=request.POST["body"],active=True)
                    return redirect(f"./{slug}")
                else:
                    messages.error(request,"نمیتوانید نظر خالی بفرستید")
                    return redirect(f"./{slug}")


            if "update_num" in request.POST:
                print(request.POST)
                print("ok")
                if request.POST["update_num"] != "":
                    print("hast")
                    update_num=int(request.POST["update_num"])
                    print(type(update_num))
                    print(update_num)
                    if update_num > 4:
                        messages.error(request,"تعداد سفارش شما بیشتر از چهار عدد نمیتواند باشد")
                        return redirect(f"./{slug}")
                    elif update_num == 0 or update_num<0:
                        print("num sefr ya manfi ast")
                        messages.error(request,"نمی تواید صفر یا منفی وارد کنید")
                        return redirect(f'./{slug}')
                    u=UserList.objects.filter(user=request.user,product=product[0],buy=True)[0]
                    u.buy_num=update_num
                    u.save()
                    return redirect(f"./{slug}")
                else:
                    return redirect(f"./{slug}")


            if "saved" in request.POST:
                print("save hast")
                print("Okkkkkkk")
                UserList.objects.create(user=request.user,product=product[0],saved=True)
                return redirect(f"./{slug}")
            



            if "del_from_saved" in request.POST:
                print("Okkkkkkk del")
                userlist=UserList.objects.filter(user=request.user,product=product[0],saved=True)
                userlist.delete()
                return redirect(f"./{slug}")
            



            
            if "buy" in request.POST:
                if request.POST["num"] != "":
                    print("num hast")
                    num=int(request.POST["num"])
                    if num > 4:
                        messages.error(request," تعداد سفارش شما بیشتر از چهار عدد نمیتواند باشد")
                        return redirect(f"./{slug}")
                    elif num == 0 or num<0:
                        print("num sefr ya manfi ast")
                        messages.error(request,"نمی تواید صفر یا منفی وارد کنید")
                        return redirect(f'./{slug}')

                    UserList.objects.create(user=request.user,product=product[0],buy=True,buy_num=num)
                else:
                    print("num nist")
                    
                    UserList.objects.create(user=request.user,product=product[0],buy=True,buy_num=1)

                return redirect(f"./{slug}")

            
            
            
            


            return redirect(f"./{slug}")
    



    if not request.user.is_anonymous:
        return render(request,"appp/detail_product.html",{"product":product,"empty_comment":empty_comment,"count":len(p_count),"empty_save":empty_save,"empty_buy":empty_buy})
    else:
        return render(request,"appp/detail_product.html",{"product":product})

@login_required
def buy_listt(request):
    products=UserList.objects.filter(user=request.user,buy=True)
    sum_price=0
    for s in products:
        print(s.buy_num)
        num=s.buy_num
        summ=num*s.product.price
        sum_price+=summ
    
    if len(products)==0:
        return render(request,"appp/buy_list.html",{"products":products})
    return render(request,"appp/buy_list.html",{"products":products,"sum_price":sum_price,"count":len(products)})

@login_required
def delete_buy_listt(request,slug):
    product=Product.objects.filter(slug=slug)
    target=UserList.objects.filter(user=request.user,product=product[0],buy=True)
    buy_list=UserList.objects.filter(user=request.user,buy=True)

    

    if request.method =="POST":
        target.delete()
        return redirect("index")
    if len(buy_list)!=0:
        return render(request,"appp/delete_buy_listt.html",{"count":len(buy_list)})
    return render(request,"appp/delete_buy_listt.html")

@login_required
def profile(request):
    saved=UserList.objects.filter(user=request.user,saved=True)
    buy_list=UserList.objects.filter(user=request.user,buy=True)

    sum_price=0
    for s in buy_list:
        print(s.buy_num)
        num=s.buy_num
        summ=num*s.product.price
        sum_price+=summ
    

    if len(buy_list)==0:
        return render(request,"appp/profile.html",{"saved":saved,"buy_list":buy_list})
    return render(request,"appp/profile.html",{"saved":saved,"buy_list":buy_list,"sum_price":sum_price,"count":len(buy_list)})




def register(request):
    if request.method=="POST":
        form=RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")        
    else:
        form=RegisterForm()
    return render(request,"appp/register.html",{"form":form})

