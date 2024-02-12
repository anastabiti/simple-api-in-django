import base64
from django.http import HttpResponse, JsonResponse
# create a user
from django.contrib.auth.models import User,Group
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render, redirect
from imagekitio import ImageKit

from asgiref.sync import sync_to_async
import environ
env = environ.Env()
# My Models 
from app.models import Products,Extended_User
def home(request):
    print(request.user.is_authenticated)
    if request.user.is_authenticated:
        return render(request, 'home.html')
    return redirect('/auth')



def create_user(request):
    if(request.method == 'POST'):
        # try:
            role  =request.POST.get("role")
            if(role == "seller"):
                group = Group.objects.get(name="sellers")
                user =User.objects.create_user(request.POST.get("username") ,request.POST.get("email"),request.POST.get("password"))
                user.groups.add(group)
                user.save()
                login(request,user)
                return redirect('/')

            else:
                return HttpResponse("no such role")
        # except:
        #     return HttpResponse("An exception occurred", status=400)
        
    if(request.method == 'GET'):  
        return render(request, 'signup_seller.html')
    

def create_user_buyer(request):
    if(request.method == 'POST'):
            role  =request.POST.get("role")
            if(role == "client"):
                group = Group.objects.get(name="buyers")
                user =User.objects.create_user(request.POST.get("username") ,request.POST.get("email"),request.POST.get("password"))
                user.groups.add(group)
                user.save()
                login(request,user)
                return redirect('/')
            else:
                return HttpResponse("no such role")
    if(request.method == 'GET'):  
        return render(request, 'signup_buyer.html')

                 
    return HttpResponse(request.POST)
def login_(request):
        print(request.method , " method")
        if(request.method == "POST"):
            user = authenticate(username=request.POST.get("username"), password=request.POST.get("password"))
            # return None if the auth failed
            if user is not None:
                login(request,user)
                return redirect('/')
            else:
                return HttpResponse('Not logged', status=401)
        if(request.method == "DELETE"):
            print("logout is called !!!+!+!+!+!+!+!++!")
            logout(request)
            return redirect('/')
        if(request.method == "GET"):
            return render(request, 'login.html')
def logout_(request):
        print(request.method , " method")
        if(request.method == "POST"):
            print("logout is called !!!+!+!+!+!+!+!++!")
            logout(request)
            return redirect('/')

def list_product(request):
    user=  request.user
    if(request.user.is_authenticated):
        if(request.method == "POST"):
            if user.groups.filter(name = "sellers").exists():
                name  =request.POST.get("name")
                price  =request.POST.get("price")
                new_product = Products(name=name, price=price, seller=user)
                new_product.save()
                return  HttpResponse("DONE : created")
        if((request.method == "GET") and (user.groups.filter(name = "sellers").exists())):
            return render(request, 'list_product.html')
        
    return HttpResponse('NOT a seller / Not logged', status=401)

def all_products(request):
    # fruits = Fruit.objects.all()
    # render(request, 'index.html', {'fruits': fruits})
    user=  request.user
    if(user.is_authenticated):
        products = Products.objects.values()
        # return render(request, 'list_product.html', {'products': products})
        return JsonResponse({'products': list(products)})
    
    

def get_all_user(request):
    user=  request.user
    if(user.is_authenticated):
        # users  = User.objects.values_list()
        users = User.objects.values('id', 'username', 'email')  
        return JsonResponse({'users':list(users)})


def uploading(request):
        if(request.user.is_authenticated):
            if(request.method == "POST"):
                file_ = request.FILES["image"]
                file_content = file_.read()
                # print(file_content)

                image_ =ImageKit(
                    private_key=env("private_key"),
                    public_key=env("public_key"),
                    url_endpoint=env("url_endpoint"),
                    )
                file_content_base64 = base64.b64encode(file_content).decode('utf-8')

                url = image_.upload(
                file=file_content_base64,
                file_name=file_.name,
                )
                print(url.url)
                f = open("result.json", "a")
                f.write(str(url.response_metadata.raw))
                f.close()
                p =Extended_User( request.user.id, image=url.url)
                # request.user.image = url.url
                p.save()
                
                # print(request.user)
                # print( request.user.image , " saved data +")
                return HttpResponse("done")
        return HttpResponse("Not logged")