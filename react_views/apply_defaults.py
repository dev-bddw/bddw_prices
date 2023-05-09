from formula_tear_sheets.models import FormulaTearSheet, json_default
from tear_sheets.models import TearSheet


# change the defaults on normal tearsheets for for normal and gbp attributes
def update_tearsheets():
    for tearsheet in TearSheet.objects.all():
        tearsheet.sdata = TearSheet.json_default()
        tearsheet.save()


def update_tearsheets_gbp():
    for tearsheet in TearSheet.objects.all():
        tearsheet.gbp_sdata = TearSheet.gbp_sdata_json_default()
        tearsheet.save()


def update_formula_tearsheets():
    for tearsheet in FormulaTearSheet.objects.all():
        tearsheet.sdata = json_default()
        tearsheet.save()
