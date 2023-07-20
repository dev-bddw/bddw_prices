import json

from django.conf import settings
from django.urls import reverse

from price_records.models import FormulaPriceListPriceRecord, PriceListPriceRecord


def return_pricelist():
    def build():
        return [
            x.to_dict()
            for x in PriceListPriceRecord.objects.exclude(
                cat_series_item__category__pricelist_ignore=True
            )
        ] + [
            x.to_dict()
            for x in FormulaPriceListPriceRecord.objects.exclude(
                cat_series_item__category__pricelist_ignore=True
            )
        ]

    return json.dumps({"pricelist": build()})


def get_url_for_print(url_code):

    url_string = settings.PDF_APP_URL + settings.SITE_URL
    url_string += reverse(url_code)

    return url_string
