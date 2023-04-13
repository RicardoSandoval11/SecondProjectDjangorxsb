from django.contrib import admin

#import models
from .models import User, Interest, Token

# Register your models here.
admin.site.register(User)
admin.site.register(Interest)
admin.site.register(Token)
