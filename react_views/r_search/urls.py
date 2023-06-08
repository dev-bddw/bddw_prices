from django.urls import path

from .views import search_view_entry
from .views_api import print_api, search_api

app_name = "r_search"

# /react/search/
urlpatterns = [path("", view=search_view_entry, name="search")]

# search_api
urlpatterns += [
    path("api/search", view=search_api, name="search-api"),
    path("api/print", view=print_api, name="print-api"),
]
