from django.urls import path

from .views import detail_view_entry, edit_view_entry
from .views_api import (
    create_caption_api,
    create_detail_api,
    create_footer_api,
    edit_caption_api,
    edit_detail_api,
    edit_footer_api,
    edit_image_api,
    edit_pricerecord_api,
    edit_tearsheet_api,
)
from .views_print import (
    detail_view_for_printing,
    detail_view_for_printing_list,
    print_all,
    redirect_detail_view_to_pdf,
    redirect_detail_view_to_pdf_list,
)

app_name = "r_tear_sheets"

### REAL PATTERNS ###
urlpatterns = [
    path("edit-tearsheet/<id>", edit_view_entry, name="edit-tearsheet"),
    path("view-tearsheet/<id>", detail_view_entry, name="view-tearsheet"),
    path("print-redirect/<id>", view=redirect_detail_view_to_pdf, name="print"),
    path(
        "print-redirect-list/<id>",
        view=redirect_detail_view_to_pdf_list,
        name="print-list",
    ),
    path(
        "detail-for-print/<id>",
        view=detail_view_for_printing,
        name="detail-view-for-print",
    ),
    path(
        "print_all",
        view=print_all,
        name="print_all",
    ),
    path(
        "detail-for-print-list/<id>",
        view=detail_view_for_printing_list,
        name="detail-view-for-print-list",
    ),
]

### API URLS ###
urlpatterns += [
    path("edit-tearsheetapi/<id>", edit_tearsheet_api, name="edit-tearsheet-api"),
    path("edit-image/<id>", edit_image_api, name="edit-image-api"),
    path("edit-price-record/", edit_pricerecord_api, name="edit-pricerecord-api"),
    path("edit-caption-record/", edit_caption_api, name="edit-caption-api"),
    path("edit-detail-record/", edit_detail_api, name="edit-detail-api"),
    path("edit-footer-record/", edit_footer_api, name="edit-footer-api"),
    path("create-footer-record/<id>", create_footer_api, name="create-footer-api"),
    path("create-detail-record/<id>", create_detail_api, name="create-detail-api"),
    path(
        "create-caption-record/<id>",
        create_caption_api,
        name="create-caption-api",
    ),
]
