from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Profile

# Register your models here.

admin.site.register(Profile)
admin.site.unregister(Group)