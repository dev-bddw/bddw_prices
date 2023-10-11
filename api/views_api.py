from django.http import JsonResponse

from rest_framework.decorators import api_view

from .helpers import return_sheet_data

@api_view(['GET'])
def tearsheet_api(request, tearsheet_slug):
    """
    send back info about a tearsheet
    lookup is performed by title
    """
    if request.method == "GET":
        data = return_sheet_data(tearsheet_slug)

        return JsonResponse({'data': data})

