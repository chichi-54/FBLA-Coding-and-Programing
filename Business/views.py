from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .utils import search_businesses, paginate_businesses
from .models import Business

@login_required(login_url="login")
def home(request):
    businesses , search_query = search_businesses(request)
    custom_range, businesses = paginate_businesses(request, businesses, 6)
    context = {'businesses':businesses, 'search_query':search_query, 'custom_range':custom_range}
    return render(request, "business/home.html", context)


@login_required(login_url="login")
def single_business(request, pk):
    businessObj = Business.objects.get(id=pk)
    context = {'business':businessObj}
    return render(request, "business/single_business.html", context)


@login_required(login_url="login")
def create_business(request):
    context = {}
    return render(request, "business/business_form.html", context)


@login_required(login_url="login")
def update_business(request, pk):
    context = {}
    return render(request, "business/business_form.html", context)


@login_required(login_url="login")
def delete_business(request, pk):
    context = {}
    return render(request, "business/business_form.html", context)


@login_required(login_url="login")
def inbox(request):
    context = {}
    return render(request, "business/inbox.html", context)
