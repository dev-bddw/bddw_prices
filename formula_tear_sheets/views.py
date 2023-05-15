from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import FormulaTearSheet


@login_required
def list_view(request):

    return render(
        request,
        "formula_tear_sheets/list_view.html",
        {
            "tearsheets": FormulaTearSheet.objects.all(),
        },
    )
