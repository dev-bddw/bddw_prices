from django.urls import path

from tear_sheets.gbp.views import (  # views; edit views; pdf printing views
    detail_view,
    detail_view_for_printing,
    detail_view_for_printing_list,
    list_view,
    print_all,
    redirect_detail_view_to_pdf,
    redirect_detail_view_to_pdf_list,
)

app_name = "gbp"

urlpatterns = [
    path("list/", view=list_view, name="list"),
    path("detail/<pk>", view=detail_view, name="detail"),
    path("print-redirect/<pk>", view=redirect_detail_view_to_pdf, name="print"),
    path(
        "print-redirect-list/<pk>",
        view=redirect_detail_view_to_pdf_list,
        name="print-list",
    ),
    path(
        "detail-for-print/<pk>",
        view=detail_view_for_printing,
        name="detail-view-for-print",
    ),
    path(
        "detail-for-print-list/<pk>",
        view=detail_view_for_printing_list,
        name="detail-view-for-print-list",
    ),
    path(
        "print_all",
        view=print_all,
        name="print_all",
    ),
]
