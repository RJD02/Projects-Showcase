from .forms import CustomUserCreationForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .models import Profile
from users.models import User

# Create your views here.


def profiles(request):
    profiles = Profile.objects.all
    context = {'profiles': profiles}
    return render(request, 'users/profiles.html', context)


def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)

    # skills_with_description = [
    #     skill for skill in profile.skill_set.all() if skill.description]
    top_skills = profile.skill_set.exclude(description__exact='')

    # other_skills = [
    #     skill for skill in profile.skill_set.all() if skill.description == '']
    other_skills = profile.skill_set.filter(description='')

    context = {'profile': profile, 'top_skills': top_skills,
               'other_skills': other_skills}

    return render(request, 'users/user-profile.html', context)


def login_user(request):
    page = 'login'
    context = {'page': page}

    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        print(request.POST)
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('profiles')
        else:
            # User does not exist
            messages.error(request, 'User name or password is wrong')

    return render(request, 'users/login_register.html', context)


def logout_user(request):
    logout(request)
    messages.success(request, 'User was logged out')
    return redirect('login')


def register_user(request):
    page = 'register'
    context = {'page': page}
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'Account was succesfully created!')

            login(request, user)
            return redirect('edit-account')
        else:
            messages.error(request, 'Error occurred during form registration')

    context['form'] = form
    return render(request, 'users/login_register.html', context)


@login_required(login_url='login')
def create_skill(request):
    profile = request.user.profile
    form = SkillForm()
    if request.method == "POST":
        form = SkillForm(request.POST, request.FILES)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, 'Skill was successfully added')
            return redirect('account')
    context = {'form': form}
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def update_skill(request, pk):
    profile = request.user.profile
    # print(profile.skill_set.get())
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill was successfully updated')
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def delete_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == "POST":
        skill.delete()
        messages.success(request, 'Skill was successfully deleted')
        return redirect('account')
    context = {'object': skill, 'name': skill}
    return render(request, 'delete_template.html', context)
