from django.shortcuts import render, redirect, get_object_or_404
from Users.models import Profile
from django.core.signing import Signer, BadSignature
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.models import User
# Create your views here.


@login_required(login_url="login")
def all_users(request):
    profiles = Profile.objects.all()
    context = {'profiles':profiles}
    return render(request, 'admin/all_users.html', context)


@login_required(login_url="login")
def applications(request):
    context = {}
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