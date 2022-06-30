from django.shortcuts import render

# Create your views here.
from products.models import Category, CatSeriesItem


def price_list(request):

    new_dict = {}

    # we need to fix the Category sorting here in some way
    for category in Category.objects.all():
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
        "price_list.html",
        {
            "price_list_records": final_tuples,
        },
    )
