from django.urls import path

# import views
from .views import (
    ListEntriesApiView,
    EntryDetailView,
    ListEntriesFilteredByTag,
    ListMostRecentEntriesHomePage,
    EntriesByInterstsView,
    ListEntriesByCategory,
    ListAllFilteredEntries,
    ListMyEntries,
    DeleteEntryView,
    ListMyEntriesUserDashboard,
    GetEntryToUpdateView,
    UpdateEntryView,
    CreateEntryView,
    # categories views
    List20CategoriesHomePage,
    ListAllCategories,
    SimpleListcategoriesView,
    # tags views
    ListAllTags
)

urlpatterns = [
    path(
        'api/entry/list-all/',
        ListEntriesApiView.as_view(),
        name='list-entries'
    ),
    path(
        'api/entry/details/<pk>',
        EntryDetailView.as_view(),
        name='entry-details'
    ),
    path(
        'api/entry/filter/<pk>',
        ListEntriesFilteredByTag.as_view(),
        name='filter-entries-tag'
    ),
    path(
        'api/most-recent-entries/home',
        ListMostRecentEntriesHomePage.as_view(),
        name='most-recent-entries-home'
    ),
    path(
        'api/entries-intersts/home',
        EntriesByInterstsView.as_view(),
        name='entries-interests'
    ),
    path(
        'api/entries-by-category/<pk>',
        ListEntriesByCategory.as_view(),
        name='entries-by-category'
    ),
    path(
        'api/entries',
        ListAllFilteredEntries.as_view(),
        name='all-filtered-entries'
    ),
    path(
        'api/my-entries',
        ListMyEntries.as_view(),
        name='my-entries'
    ),
    path(
        'api/entry/delete',
        DeleteEntryView.as_view(),
        name='delete-entry'
    ),
    path(
        'api/entry/dashboard',
        ListMyEntriesUserDashboard.as_view(),
        name='my-entries-dashbaord'
    ),
    path(
        'api/entry/get-to-update',
        GetEntryToUpdateView.as_view(),
        name='get-entrie-to-update'
    ),
    path(
        'api/entry/update-entry/<pk>',
        UpdateEntryView.as_view(),
        name='update-entry'
    ),
    path(
        'api/entry/create',
        CreateEntryView.as_view(),
        name='create-entry'
    ),
    # Categories url
    path(
        'api/categories/home',
        List20CategoriesHomePage.as_view(),
        name='categories-home'
    ),
    path(
        'api/categories',
        ListAllCategories.as_view(),
        name='all-categories'
    ),
    path(
        'api/all-categories',
        SimpleListcategoriesView.as_view(),
        name='categories'
    ),
    # tags urls
    path(
        'api/tags',
        ListAllTags.as_view(),
        name='tags'
    ),
]