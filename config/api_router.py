from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter

from bddw_prices.users.api.views import UserViewSet
from csv_imports.api.views import inventory_sync
from formula_tear_sheets.api.views import (
    FormulaImageCaptionViewSet,
    FormulaTearSheetDetailViewSet,
    FormulaTearSheetFooterDetailViewSet,
    FormulaTearSheetViewSet,
)
from price_records.api.views import (
    FormulaPriceRecordViewSet,
    PriceRecordViewSet,
    TearSheetPriceRecordViewSet,
)
from products.api.views import (
    CatSeriesItemViewSet,
    CategoryViewSet,
    ItemViewSet,
    SeriesViewSet,
)
from tear_sheets.api.views import (
    ImageCaptionViewSet,
    TearSheetDetailViewSet,
    TearSheetFooterDetailViewSet,
    TearSheetViewSet,
)

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

# Users
router.register("users", UserViewSet)

# Products
router.register("categories", CategoryViewSet)
router.register("series", SeriesViewSet)
router.register("items", ItemViewSet)
router.register("cat-series-items", CatSeriesItemViewSet)

# Price Records
router.register("price-records", PriceRecordViewSet)
router.register("formula-price-records", FormulaPriceRecordViewSet)
router.register("tearsheet-price-records", TearSheetPriceRecordViewSet)

# Tear Sheets
router.register("tearsheets", TearSheetViewSet)
router.register("tearsheet-details", TearSheetDetailViewSet)
router.register("tearsheet-footer-details", TearSheetFooterDetailViewSet)
router.register("image-captions", ImageCaptionViewSet)

# Formula Tear Sheets
router.register("formula-tearsheets", FormulaTearSheetViewSet)
router.register("formula-tearsheet-details", FormulaTearSheetDetailViewSet)
router.register("formula-tearsheet-footer-details", FormulaTearSheetFooterDetailViewSet)
router.register("formula-image-captions", FormulaImageCaptionViewSet)


app_name = "api"
urlpatterns = router.urls

# Additional API endpoints (not using ViewSets)
urlpatterns += [
    path("inventory/sync/", inventory_sync, name="inventory-sync"),
]
