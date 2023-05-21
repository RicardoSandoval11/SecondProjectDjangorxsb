from django.contrib import admin

#import models
from .models import User, Interest

# Register your models here.
admin.site.register(User)
admin.site.register(Interest)
