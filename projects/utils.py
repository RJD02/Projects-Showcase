
from projects.models import Project, Tag
from django.db.models import Q

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginate_projects(request, projects, results):
    paginator = Paginator(projects, results)
    page = 1
    print('Paginator objects list', paginator.object_list,
          len(paginator.object_list))
    if request.GET.get('page'):
        page = request.GET.get('page')
        try:
            if int(page) > paginator.num_pages:
                page = paginator.num_pages
        except:
            print('Something is wrong with paginator')
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        projects = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        projects = paginator.page(page)
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
        right_index = 1
        print('Right index paginator error')

    custom_range = range(left_index, right_index + 1)
    return custom_range, projects


def search_projects(request):
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
    tags = Tag.objects.filter(name__icontains=search_query)
    projects = Project.objects.distinct().filter(Q(title__icontains=search_query)
                                                 | Q(description__icontains=search_query) | Q(tags__in=tags) | Q(owner__name__icontains=search_query) | Q(featured_image__contains='/images/'))
    return projects, search_query
