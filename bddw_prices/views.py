from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from formula_tear_sheets.models import FormulaTearSheet
from price_records.models import (
    FormulaPriceListPriceRecord,
    FormulaPriceRecord,
    PriceListPriceRecord,
    PriceRecord,
)
from products.models import CatSeriesItem
from tear_sheets.models import TearSheet


@login_required
def snapshot(request):

    return render(
        request,
        "snapshot.html",
        {
            "cat_series_items": CatSeriesItem.objects.all(),
            "cat_series_items_with_formula": [
                x for x in CatSeriesItem.objects.all() if x.has_formula()
            ],
            "tear_sheets": TearSheet.objects.all(),
            "tear_sheets__last_updated": TearSheet.objects.all()
            .order_by("updated_on")
            .last(),
            "price_records": PriceRecord.objects.all(),
            "formula_tear_sheets": FormulaTearSheet.objects.all(),
            "formula_tear_sheets__last_updated": FormulaTearSheet.objects.all()
            .order_by("updated_on")
            .last(),
            "formula_tear_sheets__price_records": FormulaPriceRecord.objects.all(),
            "pricelist_records": PriceListPriceRecord.objects.all(),
            "pricelist_records__last_updated": PriceListPriceRecord.objects.all()
            .order_by("updated_on")
            .last(),
            "formula_price_list__price_records": FormulaPriceListPriceRecord.objects.all(),
            "formula_price_list__last_updated": FormulaPriceListPriceRecord.objects.all()
            .order_by("updated_on")
            .last(),
        },
    )
