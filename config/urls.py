from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.authtoken.views import obtain_auth_token

from bddw_prices.views import snapshot
from react_views.views import (
    create_caption_api,
    create_detail_api,
    create_footer_api,
    detail_view_entry,
    edit_caption_api,
    edit_detail_api,
    edit_footer_api,
    edit_image_api,
    edit_pricerecord_api,
    edit_tearsheet_api,
    edit_view_entry,
)

urlpatterns = [
    path("", view=snapshot, name="home"),
    path(
        "about/", TemplateView.as_view(template_name="pages/about.html"), name="about"
    ),
    path("pricelists/", include("price_lists.urls", namespace="pricelists")),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    path("users/", include("bddw_prices.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),
    # Your stuff: custom urls includes go here
    path("tear-sheets/", include("tear_sheets.urls", namespace="tearsheets")),
    path("gbp/", include("tear_sheets.gbp.urls", namespace="gbp")),
    path(
        "formula-tear-sheets/",
        include("formula_tear_sheets.urls", namespace="formula_tearsheets"),
    ),
    path("uploads/", include("csv_imports.urls", namespace="csv_imports")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += [
    path("react/edit-tearsheet/<id>", edit_view_entry, name="edit-tearsheet"),
    path("react/view-tearsheet/<id>", detail_view_entry, name="view-tearsheet"),
    path("react/edit-tearsheetapi/<id>", edit_tearsheet_api, name="edit-tearsheet-api"),
    path("react/edit-image/<id>", edit_image_api, name="edit-image-api"),
    path("react/edit-price-record/", edit_pricerecord_api, name="edit-pricerecord-api"),
    path("react/edit-caption-record/", edit_caption_api, name="edit-caption-api"),
    path("react/edit-detail-record/", edit_detail_api, name="edit-detail-api"),
    path("react/edit-footer-record/", edit_footer_api, name="edit-footer-api"),
    path(
        "react/create-footer-record/<id>", create_footer_api, name="create-footer-api"
    ),
    path(
        "react/create-detail-record/<id>", create_detail_api, name="create-detail-api"
    ),
    path(
        "react/create-caption-record/<id>",
        create_caption_api,
        name="create-caption-api",
    ),
]

# API URLS
urlpatterns += [
    # API base url
    path("api/", include("config.api_router")),
    # DRF auth token
    path("auth-token/", obtain_auth_token),
    path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs",
    ),
]

# SILKY
# urlpatterns += [path("silk/", include("silk.urls", namespace="silk"))]


if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
