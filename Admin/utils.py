from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from Users.models import Profile

def paginate_profiles(request, profiles, results):
    page = request.GET.get('page')
    paginator = Paginator(profiles, results)

    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)

    leftIndex = (int(page) - 4)

    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page) + 5)

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)

    return custom_range, profiles


def search_profiles(request):
    search_query = ''
    role = request.GET.get("role")

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    # is_admin = Profile.objects.filter(is_admin__icontains=search_query)

    profiles = Profile.objects.filter(
        Q(username__icontains=search_query) |
        Q(first_name__icontains=search_query) |
        Q(last_name__icontains=search_query) 
    ).distinct()

    if role == "admin":
        profiles = profiles.filter(is_admin=True)
    elif role == "user":
        profiles = profiles.filter(is_admin=False)

    return profiles, search_query