from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .utils import search_businesses, paginate_businesses
# Create your views here.

@login_required(login_url="login")
def home(request):
    businesses , search_query = search_businesses(request)
    custom_range, businesses = paginate_businesses(request, businesses, 6)
    context = {'businesses':businesses, 'search_query':search_query, 'custom_range':custom_range}
    return render(request, "users/home.html", context)


@login_required(login_url="login")
def account(request):
    context = {}
    return render(request, "users/account.html", context)


@login_required(login_url="login")
def create_business(request):
    context = {}
    return render(request, "users/business_form.html", context)


@login_required(login_url="login")
def update_business(request, pk):
    context = {}
    return render(request, "users/business_form.html", context)


@login_required(login_url="login")
def delete_business(request, pk):
    context = {}
    return render(request, "users/business_form.html", context)


@login_required(login_url="login")
def inbox(request):
    context = {}
    return render(request, "users/inbox.html", context)


def login_user(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')

        else:
            messages.error(request, 'Username OR password is incorrect')

    return render(request, 'users/login_register.html')


def logout_user(request):
    logout(request)
    messages.info(request, 'User was logged out!')
    return redirect('login')

