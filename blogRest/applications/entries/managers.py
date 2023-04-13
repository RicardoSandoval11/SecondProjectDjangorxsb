from django.db import models
from django.db.models import Q
import datetime

class EntryManager(models.Manager):

    def filter_public_entries(self):
        return self.filter(
            public=True
        )

    def filter_entries_by_tag(self, tag_pk):
        return self.filter(
            tags__in=[tag_pk],
            public=True
        )
    
    def get_most_recent_entries(self):
        return self.filter(
            public=True).order_by('-created')[:4]
    
    def get_entries_by_user_interests(self, user):
        return self.filter(
            interests__in=user.interests.all(),
            public=True
        ).order_by('-created')[:4]
    
    def get_entries_by_category(self, categoryId):
        return self.filter(
            category=categoryId,
            public = True
        ).order_by('-created')

    def get_all_filtered_entries(self, title, content, categoryId, interest, tag, start_date, end_date):
        # first filter: filter by kwords
        result = self.filter(Q(title__icontains=title) & Q(content__icontains=content))

        #second filter: filter by category
        if categoryId != None:
            result = result.filter(category=categoryId)
        
        # Thid filter: Filter by interests
        if interest != None:
            result = result.filter(interests__in=interest)
        
        # Fourth filter: Filter by tag
        if tag != None:
            result = result.filter(tags__in=tag)
        
        # Fifth filter: Updated date
        if start_date != None and end_date != None:
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
            result = result.filter(created__range=(start_date, end_date)).order_by('-created')

        return result.filter(public=True)
    
    def get_entries_by_user(self, user):

        return self.filter(
            user=user
        ).order_by('-created')
        

class CategoryManager(models.Manager):

    def get_last_categories(self):
        return self.order_by('-name')[:20]
    
    def get_categoris_by_kword(self, kword):
        return self.filter(
            Q(name__icontains=kword) | Q(description__icontains=kword)
        ).order_by('-name')