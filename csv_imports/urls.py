from django.urls import path

from .views import upload

app_name = "csv_imports"

urlpatterns = [
    path("", view=upload, name="upload"),
]
