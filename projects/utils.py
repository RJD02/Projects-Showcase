
from projects.models import Project, Tag
from django.db.models import Q

from django.core.paginator import Paginator


def paginate_projects(request, projects, results):
    paginator = Paginator(projects, results)
    page = 1
    if request.GET.get('page'):
        page = request.GET.get('page')
        if int(page) > paginator.num_pages:
            page = paginator.num_pages

    projects = paginator.page(page)
    page = int(page)

    left_index = (page - 4)

    if left_index < 1:
        left_index = 1

    right_index = (page + 5)
    if page == 1:
        right_index = page + 6

    if right_index > paginator.num_pages:
        right_index = paginator.num_pages

    custom_range = range(left_index, right_index + 1)
    return custom_range, projects


def search_projects(request):
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
        print(search_query)
    tags = Tag.objects.filter(name__icontains=search_query)
    projects = Project.objects.distinct().filter(Q(title__icontains=search_query)
                                                 | Q(description__icontains=search_query) | Q(tags__in=tags) | Q(owner__name__icontains=search_query))
    return projects, search_query
