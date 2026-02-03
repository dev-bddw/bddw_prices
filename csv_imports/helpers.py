from price_records.models import (
    FormulaPriceRecord,
    PriceListPriceRecord,
    PriceRecord,
    TearSheetPriceRecord,
)
from products.models import Category, CatSeriesItem, Item, Series
from tear_sheets.models import TearSheet


def process_records(records: list):
    """
    iterates over records
    creates category series items
    creates tearsheet price records
    create pricelist price records
    automatically creates tearsheets for CatSeriesItems with price records
    returns report of record creation

    """
    report = []
    # Track which CatSeriesItems need tearsheets
    csi_with_tearsheet_records = set()

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
                            "gbp_price": record["gbp_price"],
                            "gbp_trade": record["gbp_trade"],
                            "gbp_price_no_vat": record["gbp_price_no_vat"],
                            "gbp_trade_no_vat": record["gbp_trade_no_vat"],
                        },
                    )
                    # Track this CatSeriesItem for tearsheet creation
                    csi_with_tearsheet_records.add(cat_series_item.pk)
                    
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
                            "gbp_price": record["gbp_price"],
                            "gbp_trade": record["gbp_trade"],
                            "gbp_price_no_vat": record["gbp_price_no_vat"],
                            "gbp_trade_no_vat": record["gbp_trade_no_vat"],
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
            else:
                # Handle formula price records
                if record["is_tearsheet"] is True:
                    # Track this CatSeriesItem for tearsheet creation
                    csi_with_tearsheet_records.add(cat_series_item.pk)

    # After processing all records, create tearsheets for CatSeriesItems with price records
    # Group by Series grouping preference
    processed_tearsheets = set()  # Track tearsheets we've already processed
    
    for csi_id in csi_with_tearsheet_records:
        cat_series_item = CatSeriesItem.objects.get(pk=csi_id)
        series = cat_series_item.series
        
        # Check if this series should be grouped by series or by item
        if series.tearsheet_grouping == Series.TearSheetGrouping.BY_SERIES.value:
            # Group by Category-Series (all items in the series together)
            tearsheet_key = (cat_series_item.category.pk, series.pk)
            tearsheet_title = f"{cat_series_item.category} - {cat_series_item.series}"
        else:
            # Group by Category-Series-Item (default behavior)
            tearsheet_key = (cat_series_item.category.pk, series.pk, cat_series_item.item.pk)
            tearsheet_title = f"{cat_series_item.category} - {cat_series_item.series} - {cat_series_item.item}"
        
        # Skip if we've already processed this tearsheet
        if tearsheet_key in processed_tearsheets:
            continue
        
        # Create or get tearsheet
        tearsheet, ts_created = TearSheet.objects.get_or_create(
            title=tearsheet_title,
            defaults={
                'template': 'B',  # default template
                'gbp_template': 'C',
            }
        )
        processed_tearsheets.add(tearsheet_key)
        
        # Get all CatSeriesItems that should be in this tearsheet
        if series.tearsheet_grouping == Series.TearSheetGrouping.BY_SERIES.value:
            # Get all items in this Category-Series combination
            csi_items = CatSeriesItem.objects.filter(
                category=cat_series_item.category,
                series=series
            )
        else:
            # Just this specific Category-Series-Item
            csi_items = CatSeriesItem.objects.filter(pk=cat_series_item.pk)
        
        # Link all relevant CatSeriesItems to tearsheet and collect price records
        all_price_records = []
        all_formula_price_records = []
        
        for csi in csi_items:
            # Link CatSeriesItem to tearsheet
            if csi.tear_sheet != tearsheet:
                csi.tear_sheet = tearsheet
                csi.save()
            
            # Collect price records for this CatSeriesItem
            all_price_records.extend(PriceRecord.objects.filter(cat_series_item=csi))
            all_formula_price_records.extend(FormulaPriceRecord.objects.filter(cat_series_item=csi))
        
        # Create TearSheetPriceRecord entries for regular price records
        for pr in all_price_records:
            TearSheetPriceRecord.objects.get_or_create(
                tear_sheet=tearsheet,
                price_record=pr,
                defaults={
                    'display_order': pr.order if pr.order else 0,
                    'is_active': True,
                }
            )
        
        # Create TearSheetPriceRecord entries for formula price records
        for fpr in all_formula_price_records:
            TearSheetPriceRecord.objects.get_or_create(
                tear_sheet=tearsheet,
                formula_price_record=fpr,
                defaults={
                    'display_order': fpr.order if fpr.order else 0,
                    'is_active': True,
                }
            )
        
        # Add tearsheet creation to report
        ts_record = {
            "type": "Tearsheet",
            "status": "created" if ts_created else "updated",
            "category": cat_series_item.category.name,
            "series": cat_series_item.series.name,
            "item": cat_series_item.item.name if series.tearsheet_grouping == Series.TearSheetGrouping.BY_ITEM.value else "All Items",
            "tearsheet_title": tearsheet_title,
            "grouping": series.get_tearsheet_grouping_display(),
        }
        report.append(ts_record)

    return report
