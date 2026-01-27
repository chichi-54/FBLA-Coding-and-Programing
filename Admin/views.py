from django.shortcuts import render, redirect, get_object_or_404
from Users.models import Profile
from django.core.signing import Signer, BadSignature
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.urls import reverse
from Business.models import Business, Category
from django.contrib.auth.models import User
from .utils import search_profiles, paginate_profiles
from Business.utils import search_businesses, paginate_businesses
# Create your views here.


@login_required(login_url="login")
def all_users(request):
    profiles, search_query = search_profiles(request)
    custom_range, profiles = paginate_profiles(request, profiles, 6)
    context = {'profiles':profiles}
    return render(request, 'admin/all_users.html', context)


@login_required(login_url="login")
def all_applications(request):
    page = ""
    # businesses = Business.objects.all()
    businesses , search_query = search_businesses(request)
    pendingCount = businesses.count()
    categories = Category.objects.all()
    category_id = request.GET.get("category")

    if category_id:
        businesses = businesses.filter(categories__id=category_id)

    context = {'businesses':businesses,'pendingCount':pendingCount, 'page':page, 'search_query':search_query, 'categories':categories}
    return render(request, 'admin/applications.html', context)


@login_required(login_url="login")
def pending_applications(request):
    page = "PENDING"
    businesses , search_query = search_businesses(request, approval_state="Pending")
    businesses = businesses.filter(approval_state="Pending")
    pendingCount = businesses.count()
    categories = Category.objects.all()
    category_id = request.GET.get("category")

    if category_id:
        businesses = businesses.filter(categories__id=category_id)

    context = {'businesses':businesses,'pendingCount':pendingCount, 'page':page, 'search_query':search_query, 'categories':categories}
    return render(request, 'admin/applications.html', context)


@login_required(login_url="login")
def approved_applications(request):
    page = "APPROVED"
    businesses , search_query = search_businesses(request)
    businesses = businesses.filter(approval_state="Approved")
    pendingCount = businesses.count()
    categories = Category.objects.all()
    category_id = request.GET.get("category")

    if category_id:
        businesses = businesses.filter(categories__id=category_id)

    context = {'businesses':businesses,'pendingCount':pendingCount, 'page':page, 'search_query':search_query, 'categories':categories}
    return render(request, 'admin/applications.html', context)


@login_required(login_url="login")
def declined_applications(request):
    page = "DECLINED"
    businesses , search_query = search_businesses(request)
    businesses = businesses.filter(approval_state="Declined")
    pendingCount = businesses.count()
    categories = Category.objects.all()
    category_id = request.GET.get("category")

    if category_id:
        businesses = businesses.filter(categories__id=category_id)

    context = {'businesses':businesses,'pendingCount':pendingCount, 'page':page, 'search_query':search_query, 'categories':categories}
    return render(request, 'admin/applications.html', context)

@login_required(login_url="login")
def make_admin(request, pk):
    profile = get_object_or_404(Profile, id=pk)
    profile.is_admin = True
    profile.save()
    messages.success(request, f"{profile.username} is now an admin")
    return redirect(request.GET.get('next'))

@login_required(login_url="login")
def remove_admin(request, pk):
    profile = get_object_or_404(Profile, id=pk)
    profile.is_admin = False
    profile.save()
    messages.error(request, f"{profile.username} is removed as admin")
    return redirect(request.GET.get('next'))


@login_required(login_url="login")
def approve_business(request, pk):
    business = get_object_or_404(Business, id=pk)
    business.approval_state = "Approved"
    business.save()
    messages.success(request, f"{business.name}'s application is now approved")
    return redirect(request.GET.get('next'))


@login_required(login_url="login")
def decline_business(request, pk):
    business = get_object_or_404(Business, id=pk)
    business.approval_state = "Declined"
    business.save()
    messages.error(request, f"{business.name}'s application is now declined")
    return redirect(request.GET.get('next'))