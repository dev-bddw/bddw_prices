from price_record.models import FormulaPriceRecord

from formula_tear_sheets.models import (
    FormulaTearSheet,
    gbp_sdata_json_default,
    json_default,
)
from tear_sheets.models import TearSheet


# funcs must be imported and run in django shell
# this file provides functions to help with updating the live site
# change the defaults on normal tearsheets for for normal and gbp attributes
def update_tearsheets():
    """
    set the default values for tearsheets
    probably not ncecessary
    """
    for tearsheet in TearSheet.objects.all():
        tearsheet.sdata = TearSheet.json_default()
        tearsheet.save()


def update_tearsheets_gbp():
    """
    set defaults for the new fields on tearsheets related to gbp data

    """

    for tearsheet in TearSheet.objects.all():
        tearsheet.gbp_sdata = TearSheet.gbp_sdata_json_default()
        tearsheet.gbp_template = "C"
        tearsheet.save()


def update_formula_tearsheets():
    """
    and do the same for formula tearsheets
    """
    for record in FormulaPriceRecord.objects.all():
        record.save()

    for tearsheet in FormulaTearSheet.objects.all():
        tearsheet.sdata = json_default()
        tearsheet.gbp_data = gbp_sdata_json_default()
        tearsheet.gbp_template = "C"
        tearsheet.save()
