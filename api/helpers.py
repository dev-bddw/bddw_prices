import json

from rest_framework.authtoken.models import Token

from price_records.models import PriceRecord
from products.models import CatSeriesItem
from tear_sheets.models import (
    ImageCaption,
    TearSheet,
    TearSheetDetail,
    TearSheetFooterDetail,
)



def return_sheet_data(name):
    """
    builds context str for react consumption

    {
        "tearsheet": {
            "id": id,
            "title": x.title,
            "img": x.image.url,
            "price_records": price_records(),
            "captions": captions(),
            "details": details(),
            "footer_details": footer_details(),
    },

    """

    def get_tearsheet(slug):
        name = ' '.join(slug.split('-'))
        try:
            return TearSheet.objects.get(title__iexact=name)
        except TearSheet.DoesNotExist:
            return None

    def price_records(id):
        """
        get all price records for tearsheet, sorted by rule type
        pricerecords are linked to tearsheet through category series item

        """

        price_records = return_price_records_by_rule_type(id)

        return price_records if price_records is not None else []

    def captions(id):
        """
        get all captions for tearsheet

        """

        captions = ImageCaption.objects.filter(tear_sheet_id=id)

        return (
            [
                {"id": c.id, "caption_title": c.caption_title, "caption": c.caption}
                for c in captions
            ]
            if captions is not None
            else []
        )  # noqa

    def details(id):
        """
        get all details for tearsheet
        sorted by title

        """

        details = return_details_by_title(id)

        return details if details is not None else []

    def footer_details(id):
        """
        get all footer details for tearsheet

        """

        footer_details = TearSheetFooterDetail.objects.filter(tear_sheet_id=id)

        return (
            [{"id": f.id, "name": f.name, "details": f.details} for f in footer_details]
            if footer_details is not None
            else []
        )


    def build_response():
        x = get_tearsheet(name)
        if x is not None:
            id = x.id
            return {
                    #"auth_token": get_or_create_token(),
                    "tearsheet": {
                        "id": x.id,
                        "title": x.title,
                        #"sdata": x.sdata,
                        #"template": x.template,
                        "img": x.image.url,
                        "price_records": price_records(id),
                        "captions": captions(id),
                        "details": details(id),
                        "footer_details": footer_details(id),
                    },
                }
        else:
            return {'error': 'Failed to find tearsheet'}

    return build_response()

def return_price_records_by_rule_type(pk: int):
    """
    lookup all pricerecords using tearsheet pk
    organize into dict by rule type

    """
    category_series_items = CatSeriesItem.objects.filter(tear_sheet=pk)

    if len(category_series_items) != 0:
        list_of_price_records = PriceRecord.objects.filter(
            cat_series_item__in=category_series_items
        )

        rule_types = []

        for x in list_of_price_records:
            if x.rule_type not in rule_types:
                rule_types.append(x.rule_type)

        price_records = []

        for p in rule_types:
            price_records.append(
                [{
                    "id": y.id,
                    "list_price": y.list_price,
                    "net_price": y.net_price,
                    "rule_type": y.rule_type,
                    "rule_display_1": y.rule_display_1,
                    "rule_display_2": y.rule_display_2,
                }
                for y in list_of_price_records
                if y.rule_type == p
                 ]
            )
        return price_records

    else:
        return None


def return_details_by_title(pk: int):
    """
    lookup all detail records by tearsheek pk
    organize into dict by title
    """

    details = TearSheetDetail.objects.filter(tear_sheet__pk=pk)

    if len(details) != 0:
        names = []

        for x in details:
            if x.name not in names:
                names.append(x.name)
        detail_records = []
        for p in names:
            detail_records.append(
                    [
                        {"id": x.id, "name": x.name, "details": x.details}
                        for x in details
                        if x.name == p
                    ]
            )

        return detail_records

    else:
        return None
