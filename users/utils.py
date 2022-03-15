from users.models import Profile, Skill
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginate_profiles(request, profiles, results):
    paginator = Paginator(profiles, results)
    page = 1
    if request.GET.get('page'):
        page = request.GET.get('page')
        if int(page) > paginator.num_pages:
            page = paginator.num_pages
    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)
    except:
        print('General except for paginator')
    page = int(page)

    left_index = (page - 4)

    if left_index < 1:
        left_index = 1

    right_index = (page + 5)
    if page == 1:
        right_index = page + 6
    try:
        if right_index > paginator.num_pages:
            right_index = paginator.num_pages
    except:
        print('Right index paginator error')

    custom_range = range(left_index, right_index + 1)
    return custom_range, profiles


def search_profiles(request):
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
        print(search_query)

    skills = Skill.objects.filter(name__icontains=search_query)

    # profiles = Profile.objects.filter(name__icontains=search_query)
    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search_query) | Q(about__icontains=search_query) | Q(skill__in=skills))
    return profiles, search_query
