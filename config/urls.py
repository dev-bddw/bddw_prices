from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views

from react_views.r_search.views import search_view_entry

# home page
urlpatterns = [path("", view=search_view_entry, name="home")]

# most of the frontend views for this site go through react_views urls.py
urlpatterns += [
    path("react/", include("react_views.urls", namespace="react_views")),
]

urlpatterns += [
    path('api/v1/', include("api.urls", namespace="api"))
    ]

# other views
urlpatterns += [
    path("pricelists/", include("price_lists.urls", namespace="pricelists")),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # login and authenticate
    path("users/", include("bddw_prices.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),
    # Your stuff: custom urls includes go here
    path("uploads/", include("csv_imports.urls", namespace="csv_imports")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

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
