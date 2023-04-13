from django.db import models

class FavoritesManager(models.Manager):

    def get_number_of_users_per_entry(self):
        return self.annotate(
            num_favorites=models.Count('user')
        ).order_by('-num_favorites')[:1]
    
    def get_favorites_per_user(self, user):
        return self.filter(
            user=user
        )