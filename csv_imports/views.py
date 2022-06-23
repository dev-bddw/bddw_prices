import csv
import datetime
import io

from django.http import HttpResponse
from django.shortcuts import render

from price_records.models import FormulaPriceRecord
from products.models import Category, CatSeriesItem, Item, Series

from .helpers import process_price_list, process_tear_sheets

# Create your views here.


def upload_formula(request):

    if request.method == "POST":

        csv_file = request.FILES["file"]
        if not csv_file.name.endswith(".csv"):
            pass
            # messages.error(request, 'THIS IS NOT A CSV FILE')
        data_set = csv_file.read().decode("UTF-8")
        io_string = io.StringIO(data_set)
        next(io_string)  # hop over first row (column headers)

        report = []

        for row in csv.reader(io_string, delimiter=",", quotechar='"'):

            category = Category.objects.get(name=row[1].upper())
            series = Series.objects.get(name=row[2].upper())
            item = Item.objects.get(name=row[3].upper())

            cat_series_item = CatSeriesItem.objects.get(
                item=item.pk, category=category.pk, series=series.pk
            )
            record, created = FormulaPriceRecord.objects.update_or_create(
                pk=row[0],
                defaults={
                    "cat_series_item": cat_series_item,
                    "rule_type": int(row[4]) if row[4] != "" else "SIZES",
                    "depth": int(row[5]) if row[5] != "" else 0,
                    "length": int(row[6]) if row[6] != "" else 0,
                    "width": int(row[7]) if row[7] != "" else 0,
                    "diameter": int(row[8]) if row[8] != "" else 0,
                    "height": int(row[9]) if row[9] != "" else 0,
                    "footboard_height": int(row[10]) if row[10] != "" else 0,
                    "headboard_height": int(row[11]) if row[11] != "" else 0,
                    "headboard_width": int(row[12]) if row[12] != "" else 0,
                    "seat_fabric_yardage": int(row[13]) if row[13] != "" else 0,
                    "seat_back_height": int(row[14]) if row[14] != "" else 0,
                    "seat_height": int(row[15]) if row[15] != "" else 0,
                    "inset": int(row[16]) if row[16] != "" else 0,
                },
            )

            if created:
                report.append(f"Created formula price Record: {record}")

            else:
                report.append(f"Updated formula price record: {record}")

        return render(request, "lot-upload.html", {"report": report})


def upload(request):

    if request.method == "POST":

        csv_file = request.FILES["file"]

        data_set = csv_file.read().decode("UTF-8")

        io_string = io.StringIO(data_set)

        next(io_string)

        report = []
        TEAR_SHEET_FOR_PROCESSING = {}
        PRICE_LIST_FOR_PROCESSING = {}

        for row in csv.reader(io_string, delimiter=",", quotechar='"'):

            # TEARSHEET PRICE RECORDS
            if row[11] not in [0, "0", ""]:

                category, created = Category.objects.get_or_create(name=row[1].upper())
                series, created = Series.objects.get_or_create(name=row[2].upper())
                item, created = Item.objects.get_or_create(name=row[3].upper())

                cat_series_item, csi_created = CatSeriesItem.objects.update_or_create(
                    category=category,
                    series=series,
                    item=item,
                    defaults={"formula": row[9]},
                )

                key = str(cat_series_item.pk)

                if key not in TEAR_SHEET_FOR_PROCESSING.keys():
                    TEAR_SHEET_FOR_PROCESSING.update({f"{key}": []})

                if row[9] == "":  # if there is no formula add it to be processed
                    TEAR_SHEET_FOR_PROCESSING[key].append(row)

                if csi_created:
                    report.append(f"Created {cat_series_item}")

            # PRICE LIST PRICE RECORDS
            if row[17] not in [0, "0", ""]:
                category, cat_created = Category.objects.get_or_create(
                    name=row[1].upper()
                )
                series, series_created = Series.objects.get_or_create(
                    name=row[2].upper()
                )
                item, item_created = Item.objects.get_or_create(name=row[3].upper())

                cat_series_item, csi_created = CatSeriesItem.objects.update_or_create(
                    category=category,
                    series=series,
                    item=item,
                    defaults={"formula": row[9]},
                )

                key = str(cat_series_item.pk)

                if key not in PRICE_LIST_FOR_PROCESSING.keys():
                    PRICE_LIST_FOR_PROCESSING.update({f"{key}": []})

                if row[9] == "":  # if there is no formula add it to be processed
                    PRICE_LIST_FOR_PROCESSING[key].append(row)

                if csi_created:
                    report.append(f"Created {cat_series_item}")

        report += process_tear_sheets(TEAR_SHEET_FOR_PROCESSING)
        report += process_price_list(PRICE_LIST_FOR_PROCESSING)

        return render(request, "lot-upload.html", {"report": report})

    else:
        return render(request, "lot-upload.html", {})


def export_formula_price_records(request):

    records = FormulaPriceRecord.objects.all().values_list(
        "id",
        "rule_type",
        "depth",
        "length",
        "width",
        "diameter",
        "height",
        "footboard_height",
        "headboard_height",
        "headboard_width",
        "seat_fabric_yardage",
        "seat_back_height",
        "seat_height",
        "inset",
    )
    date = datetime.datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")

    response = HttpResponse(
        content_type="text/csv",
        headers={
            "Content-Disposition": f'attachment; filename="FORM-PRICE-RECORDS-{date}.csv"'
        },
    )

    writer = csv.writer(response)

    writer.writerow(
        [
            "id",
            "category",
            "series",
            "item",
            "rule_type",
            "depth",
            "length",
            "width",
            "diameter",
            "height",
            "footboard_height",
            "headboard_height",
            "headboard_width",
            "seat_fabric_yardage",
            "seat_back_height",
            "seat_height",
            "inset",
        ]
    )

    for record in records:
        record = list(record)
        this_record = FormulaPriceRecord.objects.get(id=record[0])

        record.insert(1, this_record.cat_series_item.item.name)
        record.insert(1, this_record.cat_series_item.series.name)
        record.insert(1, this_record.cat_series_item.category.name)

        for i in range(len(record)):
            if record[i] == 0:
                record[i] = ""
        writer.writerow(record)

    return response


def formula_records_template(request):

    date = datetime.datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")
    response = HttpResponse(
        content_type="text/csv",
        headers={
            "Content-Disposition": f'attachment; filename="FORM-PRICE-RECORDS-{date}.csv"'
        },
    )

    writer = csv.writer(response)

    writer.writerow(
        [
            "id",
            "category",
            "series",
            "item",
            "rule_type rule_type (default: 'sizes')",
            "depth",
            "length",
            "width",
            "diameter",
            "height",
            "footboard_height",
            "headboard_height",
            "headboard_width",
            "seat_fabric_yardage",
            "seat_back_height",
            "seat_height",
            "inset",
        ]
    )

    return response


def price_records_template(request):

    date = datetime.datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")
    response = HttpResponse(
        content_type="text/csv",
        headers={
            "Content-Disposition": f'attachment; filename="PRICE-RULES-{date}.csv"'
        },
    )

    writer = csv.writer(response)

    writer.writerow(
        [
            "id",
            "category",
            "series",
            "item",
            "product_attribute1",
            "allowed_value1",
            "product_attribute2",
            "allowed_value2",
            "base_price",
            "formula_price",
            "surcharge",
            "tearsheet_include",
            "rule_type",
            "tearsheet_rule_display_1",
            "tearsheet_rule_display_2",
            "price_list_rule_display_1",
            "price_list_rule_display_2",
            "price_list_include",
        ]
    )

    return response
