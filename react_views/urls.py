from django.urls import include, path

# /react/
app_name = "react_views"

urlpatterns = [
    path(
        "tear_sheets/",
        include("react_views.r_tear_sheets.urls", namespace="r_tear_sheets"),
    ),
    path(
        "formula_tear_sheets/",
        include(
            "react_views.r_formula_tear_sheets.urls", namespace="r_formula_tear_sheets"
        ),
    ),
    path(
        "gbp_tear_sheets/",
        include("react_views.r_tear_sheets.r_gbp.urls", namespace="r_gbp"),
    ),
    path(
        "form_gbp_tear_sheets/",
        include(
            "react_views.r_formula_tear_sheets.r_form_gbp.urls", namespace="r_form_gbp"
        ),
    ),
    path("search/", include("react_views.r_search.urls", namespace="r_search")),
]
