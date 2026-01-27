from django.shortcuts import render

# Create your views here.

def all_users(request):
    context = {}
    return render(request, 'admin/all_users.html', context)


def applications(request):
    
    context = {}
    return render(request, 'admin/applications.html', context)