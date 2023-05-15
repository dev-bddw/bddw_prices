from django.urls import path

from .views import list_view  # views; edit views; pdf printing views

app_name = "gbp"

urlpatterns = [
    path("list/", view=list_view, name="list"),
]
