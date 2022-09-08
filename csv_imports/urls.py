from django.urls import path

from .views import (
    export_all_formula_price_records,
    export_all_price_records,
    export_all_pricelist_records,
    export_sorting_records,
    formula_records_template,
    price_records_template,
    sorting_upload,
    upload,
    upload_formula_price_records,
)

app_name = "csv_imports"

urlpatterns = [
    path("", view=upload, name="upload"),
    path(
        "export-price-records",
        view=export_all_price_records,
        name="export_price_records",
    ),
    path(
        "export-pricelist-records",
        view=export_all_pricelist_records,
        name="export_pricelist_records",
    ),
    path("upload-formula/", view=upload_formula_price_records, name="upload_formula"),
    path(
        "export-form-records",
        view=export_all_formula_price_records,
        name="export_formula",
    ),
    path(
        "price-records-template/", view=formula_records_template, name="form_template"
    ),
    path("form-records-template/", view=price_records_template, name="normal_template"),
    path("sorting-upload/", view=sorting_upload, name="sorting_upload"),
    path("sorting-export/", view=export_sorting_records, name="sorting_export"),
]
