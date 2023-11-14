from django.http import JsonResponse
from django.shortcuts import HttpResponse
from rest_framework.decorators import api_view

from .helpers import return_search_results
from .helpers_print import print_tearsheets

@api_view(["POST"])
def search_api(request):
    """
    handles search filter sort
    """
    if request.method == "POST":

        query = request.data["data"]["search"]
        filter = request.data["data"]["filter"]

        # this way of combining results for upper and lowercase is causing a bug where results display twice on sort
        # tearsheets = return_search_results(query.upper(), filter) + return_search_results(query.lower(), filter)

        tearsheets = return_search_results(query.upper(), filter)

        return JsonResponse({"data": tearsheets})

    else:
        return HttpResponse("Request method not supported")


@api_view(["POST"])
def print_api(request):
    """
    returns link for rar w/ all pdfs
    """
    if request.method == "POST":

        tearsheets = request.data["data"]["tearsheets"]

        rar_url = print_tearsheets(tearsheets)

        return JsonResponse({"data": {"url": rar_url}})

    else:
        return HttpResponse("Request method not supported")
