from django.contrib import admin

# import models
from .models import *

admin.site.register(Entry)
admin.site.register(Tag)
admin.site.register(Category)
