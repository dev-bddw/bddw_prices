from django.urls import path

from formula_tear_sheets.form_gbp.views import (  # views; edit views; pdf printing views
    list_view,
    print_all,
)

app_name = "form_gbp"

urlpatterns = [
    path("list/", view=list_view, name="list"),
    path(
        "print_all",
        view=print_all,
        name="print_all",
    ),
]
