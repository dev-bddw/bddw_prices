from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from formula_tear_sheets.models import FormulaTearSheet


@login_required
def list_view(request):

    return render(
        request,
        "form_gbp_list_view.html",
        {
            "tearsheets": FormulaTearSheet.objects.all().order_by("-updated_on"),
        },
    )
