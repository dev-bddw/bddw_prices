import csv
import io

from django.shortcuts import render

from price_records.models import PriceRecord
from products.models import Category, CatSeriesItem, Item, Series

from .helpers import return_updated_list


# Create your views here.
def upload(request):

    if request.method == "POST":

        csv_file = request.FILES["file"]
        # let's check if it is a csv file
        if not csv_file.name.endswith(".csv"):
            pass
            # messages.error(request, 'THIS IS NOT A CSV FILE')
        data_set = csv_file.read().decode("UTF-8")
        # setup a stream which is when we loop through each line we are able to handle a data in a stream
        io_string = io.StringIO(data_set)
        next(io_string)

        RECORD_DICT_TBP = {}
        report = []

        for row in csv.reader(io_string, delimiter=",", quotechar='"'):
            category, created = Category.objects.get_or_create(name=row[1].upper())
            series, created = Series.objects.get_or_create(name=row[2].upper())
            item, created = Item.objects.get_or_create(name=row[3].upper())

            cat_series_item, csi_created = CatSeriesItem.objects.get_or_create(
                category=category, series=series, item=item, formula=row[9]
            )
            if csi_created:
                report.append(f"Created Category Series Item {cat_series_item}")

            if str(cat_series_item.pk) not in RECORD_DICT_TBP.keys():
                RECORD_DICT_TBP.update({str(cat_series_item.pk): []})

            # if tearsheet_included = 1 include row in list for processing
            if row[11] not in ["0", ""]:
                RECORD_DICT_TBP[str(cat_series_item.pk)].append(row)

        # process all the eligible records based on cat - series - item
        # so all records w/ same cat - series - item are processed at once
        # ( cat_id, [[row lists]])
        for x, y in RECORD_DICT_TBP.items():

            # WILL CHECK FOR FORMULA RECORD FIRST

            if len(y) == 1 and (y[0][9] is not None or ""):
                # this is a formula record
                pass

            else:

                # find the baseprice record in the group
                baseprice_record = [record for record in y if record[3] == "any"]

                # this item has a baseprice record that needs to be applied to other records
                if baseprice_record != []:

                    # remove baseprice record from records to be processed
                    z = [k for k in y if k not in baseprice_record]

                    # alter price for all records using baseprice record
                    p = [return_updated_list(baseprice_record, n) for n in z]

                    # now create records using baseprice + surcharge
                    for record in p:
                        try:
                            (
                                new_price_record,
                                created,
                            ) = PriceRecord.objects.update_or_create(
                                cat_series_item=CatSeriesItem.objects.get(pk=x),
                                rule_type=record[12],
                                list_price=record[8],
                                rule_display_1=record[13],
                                rule_display_2=record[14],
                                order=1,
                                bin_id=record[0],
                            )
                            if created:
                                report.append(
                                    f"Created Price Record {new_price_record} {record[14]}"
                                )
                            else:
                                report.append(
                                    f"Updated Price Record {new_price_record} {record[14]}"
                                )
                        except IndexError:
                            report.append(f"Something wrong happened with {record[14]}")

                else:
                    # process records normally
                    for record in y:
                        try:
                            (
                                new_price_record,
                                created,
                            ) = PriceRecord.objects.update_or_create(
                                cat_series_item=CatSeriesItem.objects.get(pk=x),
                                rule_type=record[12],
                                list_price=record[8],
                                rule_display_1=record[13],
                                rule_display_2=record[14],
                                order=1,
                                bin_id=record[0],
                            )
                            if created:
                                report.append(
                                    f"Created Price Record {new_price_record} {record[14]}"
                                )
                            else:
                                report.append(
                                    f"Updated Price Record {new_price_record} {record[14]}"
                                )
                        except IndexError:
                            report.append(f"Something wrong happened with {record[14]}")

        return render(
            request, "lot-upload.html", {"dict": RECORD_DICT_TBP, "report": report}
        )

    else:
        return render(request, "lot-upload.html", {})
