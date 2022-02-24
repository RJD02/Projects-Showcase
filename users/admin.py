from django.contrib import admin

# Register your models here.
from .models import Message, Profile, Skill

admin.site.register(Profile)
admin.site.register(Skill)
admin.site.register(Message)
