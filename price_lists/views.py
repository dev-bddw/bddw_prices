from django.shortcuts import render

# Create your views here.
from price_records.models import FormulaPriceListPriceRecord, PriceListPriceRecord


def price_list(request):

    new_dict = {}

    norm_csi = [
        x.cat_series_item
        for x in PriceListPriceRecord.objects.all().order_by("cat_series_item")
    ]
    form_csi = [
        x.cat_series_item
        for x in FormulaPriceListPriceRecord.objects.all().order_by("cat_series_item")
    ]

    for item in norm_csi:
        new_dict.update(
            {f"{item}": PriceListPriceRecord.objects.filter(cat_series_item=item)}
        )

    for item in form_csi:
        new_dict.update(
            {
                f"{item}": FormulaPriceListPriceRecord.objects.filter(
                    cat_series_item=item
                )
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
