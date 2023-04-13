from django.contrib import admin

# Import models
from .models import Favorite

admin.site.register(Favorite)
