from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from tear_sheets.models import TearSheet


@login_required
def list_view(request):

    return render(
        request,
        "gbp_list_view.html",
        {
            "tearsheets": TearSheet.objects.all().order_by("-updated_on"),
        },
    )
