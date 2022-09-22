from django.urls import path

from .views import (
    change_caption_hx,
    change_detail_hx,
    change_footer_detail_hx,
    change_image_hx,
    change_price_record_hx,
    change_template_hx,
    change_title_hx,
    create_caption_hx,
    create_detail_hx,
    create_footer_detail_hx,
    detail_view,
    detail_view_for_printing,
    detail_view_for_printing_list,
    edit_view,
    list_view,
    redirect_detail_view_to_pdf,
    redirect_detail_view_to_pdf_list,
)

app_name = "formula_tearsheets"

urlpatterns = [
    path("list/", view=list_view, name="list"),
    path("detail/<pk>", view=detail_view, name="detail"),
    path("edit/<pk>", view=edit_view, name="edit"),
    path("change-title/<pk>", view=change_title_hx, name="change_title"),
    path("change-image-detail/<pk>", view=change_image_hx, name="change_image"),
    path("change-caption/<pk>", view=change_caption_hx, name="change_caption"),
    path("change-detail/<pk>", view=change_detail_hx, name="change_detail"),
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
        "change-price-record/<pk>",
        view=change_price_record_hx,
        name="change_price_record",
    ),
    path(
        "change-footer-detail/<pk>",
        view=change_footer_detail_hx,
        name="change_footer_detail",
    ),
    path(
        "detail-for-print/<pk>",
        view=detail_view_for_printing,
        name="detail-view-for-print",
    ),
    path("create-caption/<pk>", view=create_caption_hx, name="create_caption"),
    path("create-detail/<pk>", view=create_detail_hx, name="create_detail"),
    path(
        "create-footer-detail/<pk>",
        view=create_footer_detail_hx,
        name="create_footer_detail",
    ),
    path("change-template/<pk>", view=change_template_hx, name="change_template"),
]
