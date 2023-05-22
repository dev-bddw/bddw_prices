from django.urls import path

from .views import list_view

app_name = "tearsheets"

urlpatterns = [path("list/", view=list_view, name="list")]
