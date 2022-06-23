from price_records.models import PriceListPriceRecord, PriceRecord
from products.models import CatSeriesItem


def return_updated_list(baseprice_record, this_record):
    new_price = int(baseprice_record[0][8]) + int(this_record[10])
    this_record[8] = new_price
    return this_record


def process_tear_sheets(TEAR_SHEET_FOR_PROCESSING):
    report = []
    for x, y in TEAR_SHEET_FOR_PROCESSING.items():
        baseprice_record = [record for record in y if record[4] == "any"]
        if baseprice_record != []:
            z = [k for k in y if k not in baseprice_record]
            p = [return_updated_list(baseprice_record, n) for n in z]
            # now create records using baseprice + surcharge
            for record in p:
                (new_price_record, created,) = PriceRecord.objects.update_or_create(
                    bin_id=record[0],
                    defaults={
                        "cat_series_item": CatSeriesItem.objects.get(pk=x),
                        "rule_type": record[12],
                        "list_price": record[8],
                        "rule_display_1": record[13],
                        "rule_display_2": record[14],
                        "order": 1,
                    },
                )
        else:
            # process records normally
            for record in y:
                (new_price_record, created,) = PriceRecord.objects.update_or_create(
                    bin_id=record[0],
                    defaults={
                        "cat_series_item": CatSeriesItem.objects.get(pk=x),
                        "rule_type": record[12],
                        "list_price": record[8],
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
        baseprice_record = [record for record in y if record[4] == "any"]
        if baseprice_record != []:
            z = [k for k in y if k not in baseprice_record]
            p = [return_updated_list(baseprice_record, n) for n in z]
            for record in p:
                (
                    new_price_record,
                    created,
                ) = PriceListPriceRecord.objects.update_or_create(
                    bin_id=record[0],
                    defaults={
                        "cat_series_item": CatSeriesItem.objects.get(pk=x),
                        "rule_type": record[12],
                        "list_price": record[8],
                        "rule_display_1": record[15],
                        "rule_display_2": record[16],
                        "order": 1,
                    },
                )

        else:
            for record in y:
                (
                    new_price_record,
                    created,
                ) = PriceListPriceRecord.objects.update_or_create(
                    bin_id=record[0],
                    defaults={
                        "cat_series_item": CatSeriesItem.objects.get(pk=x),
                        "rule_type": record[12],
                        "list_price": record[8],
                        "rule_display_1": record[15],
                        "rule_display_2": record[16],
                        "order": 1,
                    },
                )

        if created:
            report.append(f"Created {new_price_record} (Pricelist)")
        if not created:
            report.append(f"Updated {new_price_record} (Pricelist)")

    return report
