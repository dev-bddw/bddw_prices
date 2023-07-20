from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .helpers import get_url_for_print, return_pricelist


@login_required
def list_entry(request):

    print_url = get_url_for_print("react_views:r_price_lists:print")
    print_gbp_url = get_url_for_print("react_views:r_price_lists:print-gbp")

    return render(
        request,
        "r_price_lists/pricelist/dist/index.html",
        {
            "print_url": print_url,
            "print_gbp_url": print_gbp_url,
            "context": return_pricelist(),
        },
    )


def print(request):
    return render(
        request,
        "r_price_lists/pricelist_print/dist/index.html",
        {"context": return_pricelist()},
    )


def print_gbp(request):
    return render(
        request,
        "r_price_lists/pricelist_print_gbp/dist/index.html",
        {"context": return_pricelist()},
    )
