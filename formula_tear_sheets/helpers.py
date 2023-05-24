from price_records.models import FormulaPriceRecord
from products.models import CatSeriesItem

from .models import FormulaTearSheet, FormulaTearSheetDetail


def return_price_records_by_rule_type(tear_sheet_pk):
    tear_sheet = FormulaTearSheet.objects.get(pk=tear_sheet_pk)
    category_series_items = CatSeriesItem.objects.filter(formula_tear_sheet=tear_sheet)

    if len(category_series_items) != 0:
        list_of_price_records = FormulaPriceRecord.objects.filter(
            cat_series_item__in=category_series_items
        )
        rule_types = []
        for x in list_of_price_records:
            if x.rule_type not in rule_types:
                rule_types.append(x.rule_type)
        price_records = []
        for p in rule_types:
            price_records.append(
                {f"{p}": [x for x in list_of_price_records if x.rule_type == p]}
            )
        return price_records

    else:
        return None


def return_details_by_title(tear_sheet_pk):
    details = FormulaTearSheetDetail.objects.filter(tear_sheet__pk=tear_sheet_pk)
    names = []
    for x in details:
        if x.name not in names:
            names.append(x.name)
    detail_records = []
    for p in names:
        detail_records.append({f"{p}": [x for x in details if x.name == p]})
    return detail_records
