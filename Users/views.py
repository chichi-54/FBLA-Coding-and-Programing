from django.shortcuts import render
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