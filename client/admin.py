from django.contrib.auth.models import Group
from django.contrib import admin
from client.models import CustomUser

admin.site.register(CustomUser)
admin.site.unregister(Group)
