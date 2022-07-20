from django.urls import path

from .views import list, print

app_name = "pricelists"

urlpatterns = [
    path("list/", view=list, name="list"),
    path("print/", view=print, name="print"),
]
