import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view

from price_records.models import PriceRecord
from tear_sheets.models import (
    ImageCaption,
    TearSheet,
    TearSheetDetail,
    TearSheetFooterDetail,
)

from .helpers import return_details_by_title, return_price_records_by_rule_type


@login_required
def detail_view_entry(request, id):
    user = request.user

    try:
        token = Token.objects.get(user=user)
    except Token.DoesNotExist:
        token = Token.objects.create(user=user)

    if request.method == "GET":

        x = TearSheet.objects.get(id=id)

        context = {
            "auth_token": token.key,
            "tearsheet": {
                "title": x.title,
                "sdata": x.sdata,
                "template": x.template,
                "img": x.image.url,
                "price_records": return_price_records_by_rule_type(id)
                if return_price_records_by_rule_type(id) is not None
                else [],
                "captions": [
                    {"id": c.id, "caption_title": c.caption_title, "caption": c.caption}
                    for c in ImageCaption.objects.filter(tear_sheet_id=id)
                ]
                if ImageCaption.objects.filter(tear_sheet_id=id) is not None
                else [],
                "details": return_details_by_title(id)
                if return_details_by_title(id) is not None
                else [],
                "footer_details": [
                    {"id": f.id, "name": f.name, "details": f.details}
                    for f in TearSheetFooterDetail.objects.filter(tear_sheet_id=id)
                ]
                if TearSheetFooterDetail.objects.filter(tear_sheet_id=id) is not None
                else [],
            },
        }

        context = json.dumps(context)

        return render(request, "detail/dist/index.html", {"id": id, "context": context})


@login_required
def edit_view_entry(request, id):
    user = request.user

    try:
        token = Token.objects.get(user=user)
    except Token.DoesNotExist:
        token = Token.objects.create(user=user)

    if request.method == "GET":

        x = TearSheet.objects.get(id=id)

        context = {
            "auth_token": token.key,
            "tearsheet": {
                "title": x.title,
                "sdata": x.sdata,
                "template": x.template,
                "img": x.image.url,
                "price_records": return_price_records_by_rule_type(id)
                if return_price_records_by_rule_type(id) is not None
                else [],
                "captions": [
                    {"id": c.id, "caption_title": c.caption_title, "caption": c.caption}
                    for c in ImageCaption.objects.filter(tear_sheet_id=id)
                ]
                if ImageCaption.objects.filter(tear_sheet_id=id) is not None
                else [],
                "details": return_details_by_title(id)
                if return_details_by_title(id) is not None
                else [],
                "footer_details": [
                    {"id": f.id, "name": f.name, "details": f.details}
                    for f in TearSheetFooterDetail.objects.filter(tear_sheet_id=id)
                ]
                if TearSheetFooterDetail.objects.filter(tear_sheet_id=id) is not None
                else [],
            },
        }

        context = json.dumps(context)

        return render(request, "edit/dist/index.html", {"id": id, "context": context})


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
def create_caption_api(request, id):

    errors = None

    if request.method == "POST":

        # create new ImageCpation with tear_sheet_id = id

        return JsonResponse({"errors": errors})

        # return redirect(reverse('edit-tearsheet', kwargs={'id': id}))

    else:
        return HttpResponse("Request method not supported")


@api_view(["POST"])
def edit_caption_api(request):

    errors = None

    if request.method == "POST":

        print(request.data["data"])
        ImageCaption.objects.filter(id=request.data["data"]["id"]).update(
            **request.data["data"]
        )

        return JsonResponse({"errors": errors})

    else:
        return HttpResponse("Request method not supported")


@api_view(["POST"])
def create_footer_api(request, id):

    errors = None

    if request.method == "POST":

        # create new ImageCpation with tear_sheet_id = id

        return JsonResponse({"errors": errors})

        # return redirect(reverse('edit-tearsheet', kwargs={'id': id}))

    else:
        return HttpResponse("Request method not supported")


@api_view(["POST"])
def edit_footer_api(request):

    errors = None

    if request.method == "POST":

        TearSheetFooterDetail.objects.filter(id=request.data["data"]["id"]).update(
            **request.data["data"]
        )

        return JsonResponse({"errors": errors})

    else:
        return HttpResponse("Request method not supported")


@api_view(["POST"])
def create_detail_api(request, id):

    errors = None

    if request.method == "POST":

        # create new ImageCpation with tear_sheet_id = id

        return JsonResponse({"errors": errors})

        # return redirect(reverse('edit-tearsheet', kwargs={'id': id}))

    else:
        return HttpResponse("Request method not supported")


@api_view(["POST"])
def edit_detail_api(request):

    errors = None

    if request.method == "POST":

        TearSheetDetail.objects.filter(id=request.data["data"]["id"]).update(
            **request.data["data"]
        )

        return JsonResponse({"errors": errors})

    else:
        return HttpResponse("Request method not supported")


@api_view(["POST", "PUT"])
def edit_pricerecord_api(request):
    data = request.data["data"][0]

    # PUT FULL UPDATES RESOURCES
    if request.method == "POST":

        PriceRecord.objects.filter(id=data["id"]).update(**data)

        return HttpResponse(status=200)
