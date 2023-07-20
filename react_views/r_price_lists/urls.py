from django.urls import path

from .views import list_entry, print, print_gbp

app_name = "r_price_lists"

urlpatterns = [
    path("list/", view=list_entry, name="list"),
    path("print/", view=print, name="print"),
    path("print-gbp/", view=print_gbp, name="print-gbp"),
]
