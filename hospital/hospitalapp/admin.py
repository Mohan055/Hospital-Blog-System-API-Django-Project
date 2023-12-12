from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import UserProfile, Patient ,Doctor , BlogPost

# Register your models here.
admin.site.register(UserProfile),
admin.site.register(Patient),
admin.site.register(Doctor),
admin.site.register(BlogPost)
