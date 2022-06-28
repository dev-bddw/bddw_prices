from django.shortcuts import render

# Create your views here.
from products.models import Category, CatSeriesItem


def price_list(request):

    new_dict = {}

    for category in Category.objects.all():
        new_dict.update({f"{category}": {}})

        for csi in CatSeriesItem.objects.filter(category=category):
            new_dict[f"{category}"].update(
                {
                    f"{csi.return_series_item()}": [
                        [x for x in csi.pricelistpricerecord_set.all()],
                        [x for x in csi.formulapricelistpricerecord_set.all()],
                    ]
                }
            )

    final_tuples = sorted(new_dict.items(), reverse=True)

    return render(
        request,
        "price_list.html",
        {
            "price_list_records": final_tuples,
        },
    )
