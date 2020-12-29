from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login as do_login
from django.contrib.auth import logout as do_logout
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm
from .forms import FinancialDataForm
from .models import Financial


def index(request):
    return render(request, 'index.html')


def register(request):
    if request.user.is_authenticated:
        return redirect('profile')
    form = SignUpForm()
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if (form.is_valid()):
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            try:
                form.check_mail(email)
                user = User.objects.create_user(username=email, email=email, password=password,
                first_name=first_name, last_name=last_name)
                send_mail(
                    'Nuevo usuario',
                    f'Se ha registrado {user.first_name} {user.last_name}, {user.email} en Finplans',
                    'contacto.finplans@gmail.com',
                    ['contacto.finplans@gmail.com'],
                    fail_silently=False,
                )
                if user is not None:
                    do_login(request, user)
                    return redirect('profile')
                #return redirect("https://docs.google.com/forms/d/e/1FAIpQLSfTVN6PxiaZkTKmPmZdFL86Hb_Tril-_pEBtM2gV5SePkKRMg/viewform?usp=sf_link")
                return redirect('index')
            except Exception as e:
                print(e)
    return render(request, 'register.html', {'form': form})

def profile(request):
    #if not request.user.is_authenticated:
    #    return redirect('login')
    form = FinancialDataForm()

    if request.method == 'POST':
        form = FinancialDataForm(request.POST)
        #if (form.is_valid()): ver como guardar con foreign key de request.user
            #form.save()
    return render(request, 'profile.html', {'form': form})

def login(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                do_login(request, user)
                return redirect('profile')

    return render(request, "login.html", {'form': form})

def logout(request):
    do_logout(request)
    return redirect('index')