from django.shortcuts import render
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def register_page(request):
    if request.method =="POST":  
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        email=request.POST.get("email")     
        password1=request.POST.get("password1")
        password2=request.POST.get("password2")
        

        if str(password1)==str(password2):
            password=password2
            

            user=User.objects.filter(email=email)
            if user.exists():
                messages.info(request, 'Account with the email already exists')
                return redirect("/register/")

            else:
                user=User.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    username=email
                )

                user.set_password(password)
                user.save()
                messages.info(request, 'Account created Successfully!')
                return redirect('/login/')    

        else:
            messages.info(request, "Password didn't match")
            return redirect("/register/")




    return render(request, 'register.html')

def login_page(request):
    if request.method=="POST":
        email=request.POST.get("email")
        password=request.POST.get("password")

        if User.objects.filter(email=email).exists():
            user=authenticate(username=email, password=password)

            if user is None:
                messages.error(request, 'INvalid Password')

            else:
                login(request, user=user)
                return redirect('/dashboard/')

        else:
            messages.error(request, 'Invalid Email')
            return redirect('/login/')        


    return render(request, 'login.html')

@login_required(login_url='/login/')
def dashboard_page(request):
    # queryset=User.objects.all().filter(first_name='"Bikalpa"')
    # print (queryset)

    return render(request, 'dashboard.html', {'name': request.user.first_name})

@login_required(login_url='/login/')
def logout_page(request):
    logout(request)
    return redirect('/login/')

@login_required(login_url='/login/')
def video_call(request):
    return render(request, 'zigo_cloud_API.html', {'name': request.user.first_name + ""+ request.user.last_name})

@login_required(login_url='/login/')
def join_room(request):
    if request.method == 'POST':
        roomID = request.POST['roomID']
        return redirect("/meeting?roomID=" + roomID)
    return render(request, 'join_room.html')



