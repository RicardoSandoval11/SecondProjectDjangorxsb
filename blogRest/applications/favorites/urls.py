from django.urls import path

# import views
from .views import (
    ListMostLikedFavoritesView, 
    AddEntryToFavorites, 
    ShowMyFavorites, 
    RemoveEntryFromFavorites
)

urlpatterns = [
    path(
        'api/favorites/most-liked',
        ListMostLikedFavoritesView.as_view(),
        name='most-liked-entries'
    ),
    path(
        'api/favorites/add',
        AddEntryToFavorites.as_view(),
        name='add-favorite'
    ),
    path(
        'api/favorites/my-favorites',
        ShowMyFavorites.as_view(),
        name='my-favorites'
    ),
    path(
        'api/favorites/remove',
        RemoveEntryFromFavorites.as_view(),
        name='remove-favorite'
    )
]