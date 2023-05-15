from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import TearSheet


@login_required
def list_view(request):
    """
    list all tearsheets
    """
    return render(
        request,
        "list_view.html",
        {
            "tearsheets": TearSheet.objects.all().order_by("-updated_on"),
        },
    )
