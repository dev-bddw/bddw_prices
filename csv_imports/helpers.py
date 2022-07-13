from price_records.models import PriceListPriceRecord, PriceRecord
from products.models import CatSeriesItem


def return_updated_list(baseprice_record, this_record):

    baseprice_value = baseprice_record[0][8] if baseprice_record[0][8] != "" else 0
    this_record_value = this_record[10] if this_record[10] != "" else 0

    new_price = int(baseprice_value) + int(this_record_value)

    this_record[8] = new_price

    return this_record


def process_tear_sheets(TEAR_SHEET_FOR_PROCESSING):
    report = []
    for x, y in TEAR_SHEET_FOR_PROCESSING.items():

        for record in y:
            (new_price_record, created) = PriceRecord.objects.update_or_create(
                bin_id=record[0],
                defaults={
                    "cat_series_item": CatSeriesItem.objects.get(pk=x),
                    "rule_type": record[12],
                    "list_price": record[8] if record[8] != "" else record[10],
                    "rule_display_1": record[13],
                    "rule_display_2": record[14],
                    "order": 1,
                },
            )

            if created:
                report.append(f"Created {new_price_record} (Tearsheet)")
            if not created:
                report.append(f"Updated {new_price_record} (Tearsheet)")

    return report


def process_price_list(PRICE_LIST_FOR_PROCESSING):
    report = []

    for x, y in PRICE_LIST_FOR_PROCESSING.items():

        for record in y:
            (
                new_price_record,
                created,
            ) = PriceListPriceRecord.objects.update_or_create(
                bin_id=record[0],
                defaults={
                    "cat_series_item": CatSeriesItem.objects.get(pk=x),
                    "rule_type": record[12],
                    "list_price": record[8] if record[8] != "" else record[10],
                    "rule_display_1": record[16],
                    "rule_display_2": record[17],
                    "order": 1,
                },
            )

            if created:
                report.append(f"Created {new_price_record} (Pricelist)")
            if not created:
                report.append(f"Updated {new_price_record} (Pricelist)")

    return report
