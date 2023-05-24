from django.http import JsonResponse
from django.shortcuts import HttpResponse
from rest_framework.decorators import api_view

from .helpers import return_search_results


@api_view(["POST"])
def search_api(request):
    if request.method == "POST":

        query = request.data["data"]["search"]

        tearsheets = return_search_results(query.upper()) + return_search_results(
            query.lower()
        )

        return JsonResponse({"data": tearsheets})

    else:
        return HttpResponse("Request method not supported")
