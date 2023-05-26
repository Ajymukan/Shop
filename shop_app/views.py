from django.shortcuts import render,redirect
from  .models import * 
from django.contrib import  messages
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect    




def home (request):
    search = None
    if request.GET.get('q') != None:
        search = request.GET.get('q')
    else:
        search = ''


    products = Products.objects.filter(
        Q(brand__name__icontains=search),
        Q(descriptions__icontains=search),
        Q(name__icontains=search)
    )

 
    brand = Products.objects.all()

    context = {
          'products': products,
          'brand': brand,

     }
    return render (request,'body/home.html', context) 


def info (request,pk):
    product= Products.objects.get(id=pk)
    products= Products.objects.filter(brand=product.brand)
    comment= Comment.objects.filter(product=product.id)
    context = {
          'product': product,
          'products': products,
          'comment':comment,
          }


    return render (request,'body/info.html',context)

def addcomment(request,pk):
    if request.method =="POST":
        if request.POST.get('username') != '' and request.POST.get('descriptions') != '':
            Comment.objects.create(
                username = request.POST.get('username'),
                comment = request.POST.get('descriptions'),
                product= Products.objects.get(id=pk)
            ) 
            return redirect(f'/info/{pk}/')




def loginPage(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        users = None
        try:
            users = User.objects.get(email=email)
        except:
            messages.error(request, 'Email dont not exist')

        user = authenticate(request, username=users, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'username OR password does not exist')

    return render(request, 'register/login.html')



def logoutUser(request):
    logout(request)
    return redirect('home')



def registerPage(request):

    if request.method == "POST":
        form = UserCreationForm(request.POST)

        # username1 = request.POST.get('username')
        new_email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        try:

            email1 = User.objects.get(email=new_email)
            messages.error(request, "Такой пользователь уже существует!")

        except:
                if password1 == password2:
                    if form.is_valid():
                        user = form.save(commit=False)
                        user.email  =request.POST.get('email')
                        user.save()
                        return redirect('login')
                        

                else:
                    messages.error(request, "Пароли должны совпадать")
            


    return render(request, 'register/register.html')



def mycart (request):

    products = Cart.objects.filter(user = request.user)

    total_price = 0
    for  i in products:
        total_price +=i.price

    context = {
        "products": products,
        "total_price":total_price,
    }
    return render(request,'body/cart.html',context)

def addtocart(request, pk):
    product1 = Products.objects.get(id=pk)

    cart_products = Cart.objects.filter(user = request.user)
    products_id = []
    for product in cart_products:
        products_id.append(product.products.id)

    
    if request.method == "GET":
        if  pk not in products_id:
            Cart.objects.create(
                user = request.user,
                products = product1,
                price = product1.price,
                quant = 1
        )
            return redirect('/')
        else:
            return redirect('/')
        


def update(request,pk):
    cart = Cart.objects.get(id=pk)
    quant= request.GET.get('quant')

    if int(quant) != 0:
        if request.method =="GET":
            cart.quant = request.GET.get('quant')
            cart.price = cart.products.price * float(request.GET.get('quant'))
            cart.save()
            return HttpResponseRedirect('/mycart/')
    else:
        cart.delete()
        
def order (request):

    products = Order.objects.filter(user = request.user)

    context = {
        "products": products,
    }
    return render(request,'body/order.html',context)


def addOrder (request):
    cart = Cart.objects.filter(user=request.user)
    for i in cart:
        Order.objects.create(
                user = request.user,
                products =i.products ,
                price = i.price ,
                quant = i.quant
    )
        product = Products.objects.get(id= i.products.id)
        if request.method == "GET":
           product.quant = product.quant - i.quant
           product.save()

    cart.delete()
    return redirect('/mycart/') 