from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .utils import search_businesses, paginate_businesses
from .forms import BusinessForm, BusinessImageFormSet, ReviewForm
from .models import Business
from django.utils import timezone
from datetime import timedelta

@login_required(login_url="login")
def home(request):
    businesses , search_query = search_businesses(request)
    categories = Category.objects.all()
    category_id = request.GET.get("category")

    if category_id:
        businesses = businesses.filter(categories__id=category_id)

    custom_range, businesses = paginate_businesses(request, businesses, 6)
    context = {'businesses':businesses, 'search_query':search_query, 'custom_range':custom_range, 'categories':categories}
    return render(request, "business/home.html", context)



@login_required(login_url="login")
def single_business(request, pk):
    business = Business.objects.get(id=pk)
    user = request.user.profile
    form = ReviewForm()

    # Check if user can leave a review (4-hour rule)
    four_hours_ago = timezone.now() - timedelta(hours=5)
    can_review = not business.review_set.filter(owner=user, created__gte=four_hours_ago).exists()

    if request.method == 'POST' and can_review:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.owner = user
            review.business = business
            review.save()

            # Update votes immediately after saving
            business.getVoteCount

            return redirect('single-business', pk=business.id)

    context = {'business': business,'can_review': can_review, 'reviews': business.review_set.all().order_by('-created'),'form': form}
    return render(request, 'business/single_business.html', context)


@login_required(login_url="login")
def create_business(request):
    profile = request.user.profile
    form = BusinessForm()
    formset = BusinessImageFormSet()

    if request.method == 'POST':
        form = BusinessForm(request.POST, request.FILES)
        formset = BusinessImageFormSet(request.POST, request.FILES)

        if form.is_valid():
            business = form.save(commit=False)
            business.owner = profile
            business.save()

            category_ids = request.POST.get('categories', '')
            if category_ids:
                ids = category_ids.split(',')
                business.categories.set(ids)

            newcategories = request.POST.get('newcategories', '')
            if newcategories:
                for name in newcategories.replace(',', ' ').split():
                    category, _ = Category.objects.get_or_create(
                        name=name.strip()
                    )
                    business.categories.add(category)
            formset = BusinessImageFormSet(request.POST, request.FILES, instance=business)
            if formset.is_valid():
                formset.save()
                return redirect('account')

            return redirect('account')

    context = {
        'form': form,
        'categories': Category.objects.all(),
        'formset':formset
    }
    return render(request, "business/business_form.html", context)


@login_required(login_url="login")
def update_business(request, pk):
    profile = request.user.profile
    business = profile.business_set.get(id=pk)

    all_categories = Category.objects.all()
    custom_categories = business.categories.exclude(
        id__in=all_categories.values_list('id', flat=True)
    )
    selected_category_ids = list(business.categories.values_list('id', flat=True))

    if request.method == 'POST':
        form = BusinessForm(request.POST, request.FILES, instance=business)

        if form.is_valid():
            business = form.save()

            # Delete images marked for deletion
            delete_images = request.POST.getlist('delete_images')
            if delete_images:
                BusinessImage.objects.filter(id__in=delete_images, business=business).delete()

            # Handle multiple new images
            new_images = request.FILES.getlist('new_images')
            for img in new_images:
                BusinessImage.objects.create(business=business, image=img)

            # Categories from pills
            category_ids = request.POST.get('categories', '')
            if category_ids:
                business.categories.set(category_ids.split(','))

            # Custom categories from textarea
            newcategories = request.POST.get('newcategories', '')
            if newcategories:
                for name in newcategories.replace(',', ' ').split():
                    category, _ = Category.objects.get_or_create(name=name.strip())
                    business.categories.add(category)

            return redirect('account')

    else:
        form = BusinessForm(instance=business)

    context = {
        'form': form,
        'business': business,
        'categories': all_categories,
        'custom_categories': custom_categories,
        'selected_category_ids': selected_category_ids,
        'has_custom_categories': custom_categories.exists(),
    }

    return render(request, "business/business_form.html", context)



@login_required(login_url="login")
def delete_business(request, pk):
    context = {}
    return render(request, "business/business_form.html", context)


@login_required(login_url="login")
def notifications(request):
    page = 'notifications'
    profile = request.user.profile
    admin = profile.is_admin = True
    notifications = request.user.profile.notifications.order_by("-created")

    context = {'page':page, 'profile':profile, 'admin':admin, 'notifications':notifications}
    return render(request, "business/notifications.html", context)


@login_required
def mark_notification_read(request, pk):
    notification = Notification.objects.get(pk=pk, recipient=request.user)
    notification.is_read = True
    notification.save()
    return redirect("notifications")
