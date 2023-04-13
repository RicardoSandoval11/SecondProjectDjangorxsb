from django.db import models

#  import required models
from applications.users.models import User
from applications.entries.models import Entry

# import managers
from .managers import FavoritesManager


class Favorite(models.Model):

    entry = models.ForeignKey(
        Entry,
        verbose_name='Entry',
        on_delete=models.CASCADE,
        related_name='entry'
    )
    user = models.ForeignKey(
        User,
        verbose_name='User',
        on_delete=models.CASCADE,
        related_name='user'
    )
    
    objects = FavoritesManager()

    class Meta:
        verbose_name = 'Favorite'
        verbose_name_plural = 'Favorites'
        unique_together = ('entry', 'user')
    
    def __str__(self):
        return str(self.id)+' - '+self.entry.title+' - '+self.user.full_name
