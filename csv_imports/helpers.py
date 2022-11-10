from price_records.models import PriceListPriceRecord, PriceRecord
from products.models import Category, CatSeriesItem, Item, Series


def process_records(records: list):
    """
    iterates over records
    creates category series items
    creates tearsheet price records
    create pricelist price records
    returns report of record creation

    """
    report = []

    for record in records:

        if record["is_tearsheet"] or record["is_pricelist"]:

            category, created = Category.objects.get_or_create(
                name=record["category"].upper()
            )
            series, created = Series.objects.get_or_create(
                name=record["series"].upper()
            )
            item, created = Item.objects.get_or_create(name=record["item"].upper())

            cat_series_item, csi_created = CatSeriesItem.objects.update_or_create(
                category=category,
                series=series,
                item=item,
                defaults={"formula": record["formula"]},
            )

            record.update({"csi": cat_series_item.pk})

            csi_record = record.copy()
            csi_record.update(
                {
                    "type": "Cat/Series/Item",
                    "status": "updated" if csi_created is False else "created",
                }
            )
            report.append(csi_record)

            if not record["is_formula"]:

                if record["is_tearsheet"] is True:
                    (
                        new_price_record,
                        tearsheet_created,
                    ) = PriceRecord.objects.update_or_create(
                        bin_id=record["bin_id"],
                        defaults={
                            "cat_series_item": CatSeriesItem.objects.get(
                                pk=record["csi"]
                            ),
                            "rule_type": record["rule_type"],
                            "list_price": record["list_price"],
                            "rule_display_1": record["ts_rule_display_1"],
                            "rule_display_2": record["ts_rule_display_2"],
                            "order": record["order"],
                        },
                    )
                    that_record = record.copy()

                    that_record.update(
                        {
                            "status": "updated"
                            if tearsheet_created is False
                            else "created",
                            "type": "Tearsheet Record",
                        }
                    )

                    report.append(that_record)

                if record["is_pricelist"] is True:
                    (
                        new_price_record,
                        price_list_created,
                    ) = PriceListPriceRecord.objects.update_or_create(
                        bin_id=record["bin_id"],
                        defaults={
                            "cat_series_item": CatSeriesItem.objects.get(
                                pk=record["csi"]
                            ),
                            "rule_type": record["rule_type"],
                            "list_price": record["list_price"],
                            "rule_display_1": record["pl_rule_display_1"],
                            "rule_display_2": record["pl_rule_display_2"],
                            "order": record["order"],
                            "is_surcharge": record["surcharge"],
                        },
                    )
                    this_record = record.copy()

                    this_record.update(
                        {
                            "status": "updated"
                            if price_list_created is False
                            else "created",
                            "type": "Pricelist Record",
                        }
                    )

                    report.append(this_record)

    return report
