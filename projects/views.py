from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Project
from .forms import ProjectForm


def create_project(request):
    form = ProjectForm()

    print(request.POST)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('projects')

    context = {'form': form}
    return render(request, 'projects/project_form.html', context)


def update_project(request, pk):
    project = Project.objects.get(id=pk)
    form = ProjectForm(instance=project)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects')

    context = {'form': form}
    return render(request, 'projects/project_form.html', context)


def delete_project(request, pk):
    project = Project.objects.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('projects')
    return render(request, 'projects/delete_template.html', {'object': project})


def projects(request):
    projects = Project.objects.all()
    context = {
        'projects': projects
    }
    return render(request, 'projects/projects.html', context)


def project(req, id):
    projects = {}
    tags = {}
    try:
        projects = Project.objects.get(id=id)

    except:
        projects = {}
    return render(req, 'projects/single-project.html', {'project': projects})
