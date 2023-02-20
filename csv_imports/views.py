import csv
import datetime
import io

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from price_records.models import (
    FormulaPriceListPriceRecord,
    FormulaPriceRecord,
    PriceListPriceRecord,
    PriceRecord,
)
from products.models import Category, CatSeriesItem, Item, Series

from .helpers import process_records

########################
#### PRICE RECORDS #####
########################


@login_required
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
            "price_list_include",
            "price_list_rule_display_1",
            "price_list_rule_display_2",
            "gbp",
            "gbp_minus_vat",
            "gbp_trade",
            "gbp_trade_minus_vat",
        ]
    )

    return response


@login_required
def export_all_price_records(request):
    date = datetime.datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")

    response = HttpResponse(
        content_type="text/csv",
        headers={
            "Content-Disposition": f'attachment; filename="PRICE-RECORDS-{date}.csv"'
        },
    )

    writer = csv.writer(response)

    # define the db query
    price_records = PriceRecord.objects.all().values_list(
        "cat_series_item",
        "rule_type",
        "rule_display_1",
        "rule_display_2",
        "list_price",
        "net_price",
        "order",
        "bin_id",
        "is_surcharge",
    )

    date = datetime.datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")

    writer = csv.writer(response)

    # write header
    writer.writerow(
        [
            "cat_series_item",
            "rule_type",
            "rule_display_1",
            "rule_display_2",
            "list_price",
            "net_price",
            "order",
            "bin_id",
            "is_surcharge",
        ]
    )

    for record in price_records:
        record = list(record)

        record[0] = CatSeriesItem.objects.get(pk=record[0]).__str__()

        writer.writerow(record)

    return response


@login_required
def export_all_pricelist_records(request):
    date = datetime.datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")

    response = HttpResponse(
        content_type="text/csv",
        headers={
            "Content-Disposition": f'attachment; filename="PRICE-RECORDS-{date}.csv"'
        },
    )

    writer = csv.writer(response)

    # define the db query
    price_records = PriceListPriceRecord.objects.all().values_list(
        "cat_series_item",
        "rule_type",
        "rule_display_1",
        "rule_display_2",
        "list_price",
        "net_price",
        "order",
        "bin_id",
        "is_surcharge",
    )

    date = datetime.datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")

    writer = csv.writer(response)

    # write header
    writer.writerow(
        [
            "cat_series_item",
            "rule_type",
            "rule_display_1",
            "rule_display_2",
            "list_price",
            "net_price",
            "order",
            "bin_id",
            "is_surcharge",
        ]
    )

    for record in price_records:
        record = list(record)

        record[0] = CatSeriesItem.objects.get(pk=record[0]).__str__()

        writer.writerow(record)

    return response


@login_required
def upload(request):

    """
    Takes csv from bin
    creates CatSeriesItems
    creates PriceRecords
    creates PriceListPriceRecords
    returns a report on upload to the template

    """

    list_of_records = []
    empty_values = [0, "0", ""]

    columns = {
        "bin_id": 0,
        "formula": 9,
        "category": 1,
        "series": 2,
        "item": 3,
        "tearsheet": 11,
        "price_list": 15,
        "rule_type": 12,
        "ts_rule_display_1": 13,
        "ts_rule_display_2": 14,
        "pl_rule_display_1": 16,
        "pl_rule_display_2": 17,
        "list_price": 8,
        "surcharge": 10,
        "gbp": 18,
        "gbp_minus_vat": 19,
        "gbp_trade": 20,
        "gbp_trade_minus_vat": 21,
    }

    if request.method == "POST":

        csv_file = request.FILES["file"]
        data_set = csv_file.read().decode("UTF-8")
        io_string = io.StringIO(data_set)
        next(io_string)

        for row in csv.reader(io_string, delimiter=",", quotechar='"'):

            record = {
                "category": row[columns["category"]],
                "series": row[columns["series"]],
                "item": row[columns["item"]],
                "is_tearsheet": (row[columns["tearsheet"]] not in empty_values),
                "is_pricelist": (row[columns["price_list"]] not in empty_values),
                "is_formula": (row[columns["formula"]] not in empty_values),
                "formula": row[columns["formula"]],
                "bin_id": row[columns["bin_id"]],
                "rule_type": row[columns["rule_type"]],
                "list_price": row[columns["list_price"]]
                if row[columns["list_price"]] != ""
                else row[columns["surcharge"]],
                "ts_rule_display_1": row[columns["ts_rule_display_1"]],
                "ts_rule_display_2": row[columns["ts_rule_display_2"]],
                "pl_rule_display_1": row[columns["pl_rule_display_1"]],
                "pl_rule_display_2": row[columns["pl_rule_display_2"]],
                "order": 1,
                "surcharge": False if row[columns["surcharge"]] == "" else True,
                "gbp_price": row[columns["gbp"]],
                "gbp_price_no_vat": row[columns["gbp_minus_vat"]],
                "gbp_trade_no_vat": row[columns["gbp_trade_minus_vat"]],
                "gbp_trade": row[columns["gbp_trade"]],
            }

            list_of_records.append(record)

        report = process_records(list_of_records)

        return render(request, "lot-upload.html", {"report": report})

    else:

        return render(request, "lot-upload.html", {})


########################
## SORTING ##
########################


@login_required
def sorting_upload(request):

    if request.method == "POST":

        csv_file = request.FILES["file"]

        data_set = csv_file.read().decode("UTF-8")

        io_string = io.StringIO(data_set)

        next(io_string)

        report = []

        for row in csv.reader(io_string, delimiter=",", quotechar='"'):
            try:
                category, created = Category.objects.get_or_create(name=row[1].upper())
                series, created = Series.objects.get_or_create(name=row[3].upper())
                item, created = Item.objects.get_or_create(name=row[5].upper())

                cat_series_item, csi_created = CatSeriesItem.objects.update_or_create(
                    category=category,
                    series=series,
                    item=item,
                    defaults={
                        "cat_order": row[0],
                        "series_order": row[2],
                        "item_order": row[4],
                    },
                )

            except ValueError:
                report.append(
                    {
                        "type": "sorting order",
                        "category": category.name,
                        "series": series.name,
                        "item": item.name,
                        "status": "Failed",
                        "message": "Value Error",
                    }
                )

            if csi_created:
                report.append(
                    {
                        "type": "sorting order",
                        "category": category.name,
                        "series": series.name,
                        "item": item.name,
                        "status": "created",
                    }
                )
            else:
                report.append(
                    {
                        "bin_id": "n/a",
                        "type": "sorting order",
                        "category": category.name,
                        "series": series.name,
                        "item": item.name,
                        "status": "updated",
                    }
                )

        return render(request, "lot-upload.html", {"report": report})

    if request.method == "GET":

        date = datetime.datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")
        response = HttpResponse(
            content_type="text/csv",
            headers={
                "Content-Disposition": f'attachment; filename="SORTING RULES TEMPLATE-{date}.csv"'
            },
        )

        writer = csv.writer(response)

        writer.writerow(
            [
                "category_order",
                "category",
                "series_order",
                "series",
                "item_order",
                "item",
            ]
        )

        return response


@login_required
def export_sorting_records(request):
    date = datetime.datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")

    response = HttpResponse(
        content_type="text/csv",
        headers={
            "Content-Disposition": f'attachment; filename="SORTING-ORDER-{date}.csv"'
        },
    )

    writer = csv.writer(response)

    csi_records = CatSeriesItem.objects.all().values_list(
        "cat_order",
        "category",
        "series_order",
        "series",
        "item_order",
        "item",
    )

    date = datetime.datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")

    writer = csv.writer(response)

    writer.writerow(
        [
            "category_order",
            "category",
            "series_order",
            "series",
            "item_order",
            "item",
        ]
    )

    # replace pk with name of csi, write row to csv
    for record in csi_records:
        record = list(record)
        record[1] = Category.objects.get(pk=record[1]).name
        record[3] = Series.objects.get(pk=record[3]).name
        record[5] = Item.objects.get(pk=record[5]).name

        writer.writerow(record)

    return response


########################
#### FORMULA RECORDS ###
########################


@login_required
def upload_formula_price_records(request):

    columns = {
        "id": 0,
        "category": 1,
        "series": 2,
        "item": 3,
        "rule_type": 4,
        "rule_display_1": 5,
        "rule_display_2": 6,
        "tearsheet_include": 7,
        "price_list_include": 8,
        "depth": 9,
        "length": 10,
        "width": 11,
        "diameter": 12,
        "height": 13,
        "footboard_height": 14,
        "headboard_height": 15,
        "headboard_width": 16,
        "seat_fabric_yardage": 17,
        "seat_back_height": 18,
        "seat_height": 19,
        "inset": 20,
    }

    if request.method == "POST":

        csv_file = request.FILES["file"]

        data_set = csv_file.read().decode("UTF-8")
        io_string = io.StringIO(data_set)

        next(io_string)  # hop over first row

        report = []

        for row in csv.reader(io_string, delimiter=",", quotechar='"'):

            category, created = Category.objects.get_or_create(
                name=row[columns["category"]].upper()
            )
            series, created = Series.objects.get_or_create(
                name=row[columns["series"]].upper()
            )
            item, created = Item.objects.get_or_create(
                name=row[columns["item"]].upper()
            )

            cat_series_item, created = CatSeriesItem.objects.get_or_create(
                item=item, category=category, series=series
            )

            if row[columns["tearsheet_include"]] in [1, "1"]:

                (
                    tearsheet_record,
                    tsr_created,
                ) = FormulaPriceRecord.objects.update_or_create(
                    **{
                        "pk": row[0] if row[0] != "" else None,
                    },
                    defaults={
                        "cat_series_item": cat_series_item,
                        "rule_type": row[columns["rule_type"]]
                        if row[columns["rule_type"]] != ""
                        else "SIZES",
                        "rule_display_1": row[columns["rule_display_1"]]
                        if row[columns["rule_display_1"]] != ""
                        else "",
                        "rule_display_2": row[columns["rule_display_2"]]
                        if row[columns["rule_display_2"]] != ""
                        else "",
                        "depth": int(row[columns["depth"]])
                        if row[columns["depth"]] != ""
                        else 0,
                        "length": int(row[columns["length"]])
                        if row[columns["length"]] != ""
                        else 0,
                        "width": int(row[columns["width"]])
                        if row[columns["width"]] != ""
                        else 0,
                        "diameter": int(row[columns["diameter"]])
                        if row[columns["diameter"]] != ""
                        else 0,
                        "height": int(row[columns["height"]])
                        if row[columns["height"]] != ""
                        else 0,
                        "footboard_height": int(row[columns["footboard_height"]])
                        if row[columns["footboard_height"]] != ""
                        else 0,
                        "headboard_height": int(row[columns["headboard_height"]])
                        if row[columns["headboard_height"]] != ""
                        else 0,
                        "headboard_width": int(row[columns["headboard_width"]])
                        if row[columns["headboard_width"]] != ""
                        else 0,
                        "seat_fabric_yardage": int(row[columns["seat_fabric_yardage"]])
                        if row[columns["seat_fabric_yardage"]] != ""
                        else 0,
                        "seat_back_height": int(row[columns["seat_back_height"]])
                        if row[columns["seat_back_height"]] != ""
                        else 0,
                        "seat_height": int(row[columns["seat_height"]])
                        if row[columns["seat_height"]] != ""
                        else 0,
                        "inset": int(row[columns["inset"]])
                        if row[columns["inset"]] != ""
                        else 0,
                    },
                )

                if tsr_created:
                    report.append(
                        {
                            "bin_id": "n/a",
                            "type": "formula record",
                            "category": category.name,
                            "series": series.name,
                            "item": item.name,
                            "rule_display_1": tearsheet_record.rule_display_1,
                            "status": "Created",
                        }
                    )
                else:
                    report.append(
                        {
                            "bin_id": "n/a",
                            "type": "formula record",
                            "category": category.name,
                            "series": series.name,
                            "item": item.name,
                            "rule_display_1": tearsheet_record.rule_display_1,
                            "status": "Updated",
                        }
                    )

            if row[columns["price_list_include"]] in [1, "1"]:

                (
                    pricelist_record,
                    plr_created,
                ) = FormulaPriceListPriceRecord.objects.update_or_create(
                    **{
                        "pk": row[0] if row[0] != "" else None,
                    },
                    defaults={
                        "cat_series_item": cat_series_item,
                        "rule_type": row[columns["rule_type"]]
                        if row[columns["rule_type"]] != ""
                        else "SIZES",
                        "rule_display_1": row[columns["rule_display_1"]]
                        if row[columns["rule_display_1"]] != ""
                        else "",
                        "rule_display_2": row[columns["rule_display_2"]]
                        if row[columns["rule_display_2"]] != ""
                        else "",
                        "depth": int(row[columns["depth"]])
                        if row[columns["depth"]] != ""
                        else 0,
                        "length": int(row[columns["length"]])
                        if row[columns["length"]] != ""
                        else 0,
                        "width": int(row[columns["width"]])
                        if row[columns["width"]] != ""
                        else 0,
                        "diameter": int(row[columns["diameter"]])
                        if row[columns["diameter"]] != ""
                        else 0,
                        "height": int(row[columns["height"]])
                        if row[columns["height"]] != ""
                        else 0,
                        "footboard_height": int(row[columns["footboard_height"]])
                        if row[columns["footboard_height"]] != ""
                        else 0,
                        "headboard_height": int(row[columns["headboard_height"]])
                        if row[columns["headboard_height"]] != ""
                        else 0,
                        "headboard_width": int(row[columns["headboard_width"]])
                        if row[columns["headboard_width"]] != ""
                        else 0,
                        "seat_fabric_yardage": int(row[columns["seat_fabric_yardage"]])
                        if row[columns["seat_fabric_yardage"]] != ""
                        else 0,
                        "seat_back_height": int(row[columns["seat_back_height"]])
                        if row[columns["seat_back_height"]] != ""
                        else 0,
                        "seat_height": int(row[columns["seat_height"]])
                        if row[columns["seat_height"]] != ""
                        else 0,
                        "inset": int(row[columns["inset"]])
                        if row[columns["inset"]] != ""
                        else 0,
                    },
                )

                if plr_created:
                    report.append(
                        {
                            "bin_id": "n/a",
                            "type": "formula pricelist record",
                            "category": category.name,
                            "series": series.name,
                            "item": item.name,
                            "rule_display_1": pricelist_record.rule_display_1,
                            "status": "Created",
                        }
                    )
                else:
                    report.append(
                        {
                            "bin_id": "n/a",
                            "type": "formula pricelist record",
                            "category": category.name,
                            "series": series.name,
                            "item": item.name,
                            "rule_display_1": pricelist_record.rule_display_1,
                            "status": "Updated",
                        }
                    )
        return render(request, "lot-upload.html", {"report": report})


@login_required
def export_all_formula_price_records(request):

    tearsheet_records = FormulaPriceRecord.objects.all().values_list(
        "id",
        "rule_type",
        "rule_display_1",
        "rule_display_2",
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

    price_list_records = FormulaPriceListPriceRecord.objects.all().values_list(
        "id",
        "rule_type",
        "rule_display_1",
        "rule_display_2",
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
            "rule_display_1",
            "rule_display_2",
            "tearsheet_include",
            "price_list_include",
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

    for record in tearsheet_records:
        record = list(record)
        this_record = FormulaPriceRecord.objects.get(id=record[0])

        record.insert(1, this_record.cat_series_item.item.name)
        record.insert(1, this_record.cat_series_item.series.name)
        record.insert(1, this_record.cat_series_item.category.name)

        record.insert(7, 1)
        record.insert(8, "")

        for i in range(len(record)):
            if record[i] == 0:
                record[i] = ""
        writer.writerow(record)

    for price_list_record in price_list_records:
        price_list_record = list(price_list_record)
        this_record = FormulaPriceListPriceRecord.objects.get(id=price_list_record[0])

        price_list_record.insert(1, this_record.cat_series_item.item.name)
        price_list_record.insert(1, this_record.cat_series_item.series.name)
        price_list_record.insert(1, this_record.cat_series_item.category.name)

        price_list_record.insert(7, "")
        price_list_record.insert(8, 1)

        for i in range(len(price_list_record)):
            if price_list_record[i] == 0:
                price_list_record[i] = ""
        writer.writerow(price_list_record)

    return response


@login_required
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
            "rule_type (default: 'sizes')",
            "rule_display_1",
            "rule_display_2",
            "tearsheet_record",
            "price_list_record",
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
