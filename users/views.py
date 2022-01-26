
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
            messages.error('User name or password is wrong')

    return render(request, 'users/login_register.html')


def logout_user(request):
    logout(request)
    messages.success(request, 'User was logged out')
    return redirect('login')
