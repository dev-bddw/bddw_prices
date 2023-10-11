from django.urls import path
from .views_api import tearsheet_api

# /api/v1/
app_name = "api"

urlpatterns = [
    path(
        "<str:tearsheet_slug>/", view=tearsheet_api
        )
]
