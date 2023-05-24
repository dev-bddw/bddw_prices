from django.http import JsonResponse
from django.shortcuts import HttpResponse
from rest_framework.decorators import api_view

from price_records.models import PriceRecord
from tear_sheets.models import (
    ImageCaption,
    TearSheet,
    TearSheetDetail,
    TearSheetFooterDetail,
)


@api_view(["POST"])
def edit_tearsheet_api(request, id):
    if request.method == "POST":
        TearSheet.objects.filter(id=id).update(**request.data["data"])

        return JsonResponse({"errors": []})

    else:
        return HttpResponse("Request method not supported")


@api_view(["POST"])
def edit_image_api(request, id):
    if request.method == "POST":
        image = request.FILES.get("image")
        tearsheet = TearSheet.objects.get(id=id)
        tearsheet.image = image
        tearsheet.save()

        return JsonResponse({"url": tearsheet.image.url})

        # return redirect(reverse('edit-tearsheet', kwargs={'id': id}))

    else:
        return HttpResponse("Request method not supported")


@api_view(["POST"])
def edit_detail_api(request):
    errors = None

    if request.data["data"]["name"] == "" and request.data["data"]["details"] == "":
        TearSheetDetail.objects.filter(id=request.data["data"]["id"]).delete()

    else:
        TearSheetDetail.objects.filter(id=request.data["data"]["id"]).update(
            **request.data["data"]
        )

    return JsonResponse({"errors": errors})


@api_view(["POST"])
def create_detail_api(request, id):
    errors = None

    if request.method == "POST":
        order_no = len(TearSheetDetail.objects.filter(tear_sheet_id=id))
        request.data["data"].update({"order": order_no + 1})
        TearSheetDetail.objects.create(**request.data["data"])

        return JsonResponse({"errors": errors})

        # return redirect(reverse('edit-tearsheet', kwargs={'id': id}))

    else:
        return HttpResponse("Request method not supported")


@api_view(["POST"])
def create_caption_api(request, id):
    errors = None

    if request.method == "POST":
        order_no = len(ImageCaption.objects.filter(tear_sheet_id=id))
        request.data["data"].update({"order_no": order_no + 1})

        ImageCaption.objects.create(**request.data["data"])

        return JsonResponse({"errors": errors})

        # return redirect(reverse('edit-tearsheet', kwargs={'id': id}))

    else:
        return HttpResponse("Request method not supported")


@api_view(["POST"])
def edit_caption_api(request):
    errors = None

    if (
        request.data["data"]["caption_title"] == ""
        and request.data["data"]["caption"] == ""
    ):
        ImageCaption.objects.filter(id=request.data["data"]["id"]).delete()

    else:
        ImageCaption.objects.filter(id=request.data["data"]["id"]).update(
            **request.data["data"]
        )

    return JsonResponse({"errors": errors})


@api_view(["POST"])
def edit_footer_api(request):
    errors = None

    if request.data["data"]["name"] == "" and request.data["data"]["details"] == "":
        TearSheetFooterDetail.objects.filter(id=request.data["data"]["id"]).delete()

    else:
        TearSheetFooterDetail.objects.filter(id=request.data["data"]["id"]).update(
            **request.data["data"]
        )

    return JsonResponse({"errors": errors})


@api_view(["POST"])
def create_footer_api(request, id):
    errors = None

    if request.method == "POST":
        order_no = len(TearSheetFooterDetail.objects.filter(tear_sheet_id=id))
        request.data["data"].update({"order": order_no + 1})
        TearSheetFooterDetail.objects.create(**request.data["data"])

        return JsonResponse({"errors": errors})

        # return redirect(reverse('edit-tearsheet', kwargs={'id': id}))

    else:
        return HttpResponse("Request method not supported")


@api_view(["POST", "PUT"])
def edit_pricerecord_api(request):
    data = request.data["data"][0]

    # PUT FULL UPDATES RESOURCES
    if request.method == "POST":
        PriceRecord.objects.filter(id=data["id"]).update(**data)

        return HttpResponse(status=200)
