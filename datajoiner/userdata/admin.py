from django.contrib import admin

# Register your models here.
from .models import UserFileAnnotation, UserFile

admin.site.register(UserFileAnnotation)
admin.site.register(UserFile)

