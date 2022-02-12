from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator

from projects.utils import search_projects
from users.models import Skill
from .models import Project, Tag
from .forms import ProjectForm


@login_required(login_url='login')
def create_project(request):
    profile = request.user.profile
    form = ProjectForm()

    print(request.POST)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect('account')

    context = {'form': form}
    return render(request, 'projects/project_form.html', context)


@login_required(login_url='login')
def update_project(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    # project = Project.objects.get(id=pk)
    form = ProjectForm(instance=project)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects')

    context = {'form': form}
    return render(request, 'projects/project_form.html', context)


@login_required(login_url='login')
def delete_project(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('account')
    context = {'object': project, 'name': project}
    return render(request, 'delete_template.html', context)


def projects(request):
    projects, search_query = search_projects(request)

    results = 3
    paginator = Paginator(projects, results)

    page = 1
    if request.GET.get('page'):
        page = request.GET.get('page')
        if int(page) > paginator.num_pages:
            page = paginator.num_pages

    projects = paginator.page(page)

    context = {'projects': projects, 'search_query': search_query}
    return render(request, 'projects/projects.html', context)


def project(req, id):
    projects = {}
    tags = {}
    try:
        projects = Project.objects.get(id=id)

    except:
        projects = {}
    return render(req, 'projects/single-project.html', {'project': projects})
