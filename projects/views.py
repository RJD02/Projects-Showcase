from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q


from projects.utils import paginate_projects, search_projects
from users.models import Skill
from .models import Project, Review, Tag
from .forms import ProjectForm, ReviewForm


@login_required(login_url='login')
def create_project(request):
    profile = request.user.profile
    form = ProjectForm()

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

    results = 6
    custom_range, projects = paginate_projects(
        request, projects, results)

    context = {'projects': projects,
               'search_query': search_query, 'custom_range': custom_range}
    return render(request, 'projects/projects.html', context)


def project(req, id):
    projects = Project.objects.get(id=id)
    form = ReviewForm()
    if req.method == 'POST':
        form = ReviewForm(req.POST)
        review = form.save(commit=False)
        review.project = projects
        review.owner = req.user.profile
        review.save()

        projects.getVoteCount

        messages.success(req, 'Your review was successfully submitted')
        return redirect('single project', id=projects.id)

    return render(req, 'projects/single-project.html', {'project': projects, 'form': form})
