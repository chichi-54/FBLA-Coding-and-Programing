from Business.models import Business, Category
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginate_businesses(request, businesses, results):
    page = request.GET.get('page')
    paginator = Paginator(businesses, results)

    try:
        businesses = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        businesses = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        businesses = paginator.page(page)

    leftIndex = (int(page) - 4)

    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page) + 5)

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)

    return custom_range, businesses


def search_businesses(request):
    search_query = ''
    role = request.GET.get('role')

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    categories = Category.objects.filter(name__icontains=search_query)

    businesses = Business.objects.filter(
        Q(name__icontains=search_query) |
        Q(description__icontains=search_query) |
        Q(owner__first_name__icontains=search_query) |
        Q(owner__last_name__icontains=search_query) |
        Q(email__icontains=search_query) |
        Q(categories__in=categories) |
        Q(address__city__icontains=search_query) |
        Q(address__street_address__icontains=search_query) |
        Q(address__zip_code__icontains=search_query)
    ).distinct()

    # if role == "admin":
    #     profiles = profiles.filter(is_admin=True)
    # elif role == "user":
    #     profiles = profiles.filter(is_admin=False)

    return businesses, search_query