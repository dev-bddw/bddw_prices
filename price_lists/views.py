from django.shortcuts import render
from django.urls import reverse
from django.conf import settings
# Create your views here.
from products.models import Category, CatSeriesItem


def list(request):

    new_dict = {}

    # we need to fix the Category sorting here in some way
    for category in Category.objects.filter(pricelist_ignore=False):

        new_dict.update({f"{category}": {}})

        for csi in CatSeriesItem.objects.filter(category=category):
            if (
                len(csi.pricelistpricerecord_set.all()) > 0
                or len(csi.formulapricelistpricerecord_set.all()) > 0
            ):
                new_dict[f"{category}"].update(
                    {
                        f"{csi.return_series_item()}": [
                            [x for x in csi.pricelistpricerecord_set.all()],
                            [x for x in csi.formulapricelistpricerecord_set.all()],
                        ]
                    }
                )

    empty_series_items = []

    # remove empty series item dictionaries
    for key, value in new_dict.items():
        for series_item, lists in value.items():
            if lists == [[], []]:
                empty_series_items.append(series_item)

    final_tuples = new_dict.items()

    url_string = settings.PDF_APP_URL + settings.SITE_URL

    return render(
        request,
        "price_list.html",
        {
            "price_list_records": final_tuples,
            "print_url": url_string
            + reverse("pricelists:print")
            + "&pdf.margin.bottom=75px&pdf.margin.top=75px&pdf.margin.right=55px",
        },
    )


def print(request):

    new_dict = {}

    for category in Category.objects.filter(pricelist_ignore=False):

        new_dict.update({f"{category}": {}})

        for csi in CatSeriesItem.objects.filter(category=category):
            if (
                len(csi.pricelistpricerecord_set.all()) > 0
                or len(csi.formulapricelistpricerecord_set.all()) > 0
            ):
                new_dict[f"{category}"].update(
                    {
                        f"{csi.return_series_item()}": [
                            [x for x in csi.pricelistpricerecord_set.all()],
                            [x for x in csi.formulapricelistpricerecord_set.all()],
                        ]
                    }
                )

    empty_series_items = []

    # remove empty series item dictionaries
    for key, value in new_dict.items():
        for series_item, lists in value.items():
            if lists == [[], []]:
                empty_series_items.append(series_item)

    final_tuples = new_dict.items()

    return render(
        request,
        "price_list_print.html",
        {
            "price_list_records": final_tuples,
        },
    )
