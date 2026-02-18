import json

from django.http import JsonResponse
from django.shortcuts import HttpResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import FormParser, MultiPartParser

from django.core.files.storage import default_storage

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
        data = request.data.get("data") or {}
        template = data.get("template")
        sdata = data.get("sdata")
        update_kwargs = {}
        if template is not None:
            update_kwargs["template"] = template
        if sdata is not None:
            update_kwargs["sdata"] = sdata
        if update_kwargs:
            TearSheet.objects.filter(id=id).update(**update_kwargs)
        return JsonResponse({"errors": []})
    else:
        return HttpResponse("Request method not supported")


@api_view(["POST"])
@parser_classes([MultiPartParser, FormParser])
def edit_image_api(request, id):
    if request.method == "POST":
        image = request.FILES.get("image")
        if not image:
            return JsonResponse({"error": "No image file"}, status=400)
        tearsheet = TearSheet.objects.get(id=id)
        tearsheet.image = image
        tearsheet.save()
        # Return absolute URL so the image loads regardless of how the client is hosted
        url = request.build_absolute_uri(tearsheet.image.url)
        return JsonResponse({"url": url})
    else:
        return HttpResponse("Request method not supported")


@api_view(["POST"])
@parser_classes([MultiPartParser, FormParser])
def edit_pane_image_api(request, id):
    """Upload image for a specific pane; returns URL. pane_path is JSON array e.g. [0] or [1,0]."""
    if request.method != "POST":
        return HttpResponse("Request method not supported")
    image = request.FILES.get("image")
    if not image:
        return JsonResponse({"error": "No image file"}, status=400)
    pane_path = request.POST.get("pane_path")
    if pane_path is None:
        return JsonResponse({"error": "Missing pane_path"}, status=400)
    try:
        path_list = json.loads(pane_path)
        if not isinstance(path_list, list):
            raise ValueError("pane_path must be a list")
    except (json.JSONDecodeError, ValueError) as e:
        return JsonResponse({"error": f"Invalid pane_path: {e}"}, status=400)
    ext = image.name.split(".")[-1] if "." in image.name else "jpg"
    if ext.lower() not in ("jpg", "jpeg", "png", "gif"):
        ext = "jpg"
    path_suffix = "_".join(str(p) for p in path_list)
    storage_path = f"tear-sheet-images/ts_{id}/pane_{path_suffix}.{ext}"
    default_storage.save(storage_path, image)
    url = request.build_absolute_uri(default_storage.url(storage_path))
    return JsonResponse({"url": url})


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
