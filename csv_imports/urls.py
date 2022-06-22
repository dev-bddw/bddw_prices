from django.urls import path

from .views import (
    export_formula_price_records,
    formula_records_template,
    price_records_template,
    upload,
    upload_formula,
)

app_name = "csv_imports"

urlpatterns = [
    path("", view=upload, name="upload"),
    path("upload-formula/", view=upload_formula, name="upload_formula"),
    path(
        "export-form-records", view=export_formula_price_records, name="export_formula"
    ),
    path(
        "price-records-template/", view=formula_records_template, name="form_template"
    ),
    path("form-records-template/", view=price_records_template, name="normal_template"),
]
