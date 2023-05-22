from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view

from formula_tear_sheets.models import (
    FormulaImageCaption,
    FormulaTearSheet,
    FormulaTearSheetDetail,
    FormulaTearSheetFooterDetail,
)


@api_view(["POST"])
def edit_tearsheet_api(request, id):

    if request.method == "POST":
        print(request.data["data"])

        FormulaTearSheet.objects.filter(id=id).update(**request.data["data"])

        return JsonResponse({"errors": []})

    else:
        return HttpResponse("Request method not supported")


@api_view(["POST"])
def edit_image_api(request, id):

    if request.method == "POST":

        image = request.FILES.get("image")
        tearsheet = FormulaTearSheet.objects.get(id=id)
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

        FormulaTearSheetDetail.objects.filter(id=request.data["data"]["id"]).delete()

    else:

        FormulaTearSheetDetail.objects.filter(id=request.data["data"]["id"]).update(
            **request.data["data"]
        )

    return JsonResponse({"errors": errors})


@api_view(["POST"])
def create_detail_api(request, id):

    errors = None

    if request.method == "POST":

        order_no = len(FormulaTearSheetDetail.objects.filter(tear_sheet_id=id))
        request.data["data"].update({"order": order_no + 1})
        FormulaTearSheetDetail.objects.create(**request.data["data"])

        return JsonResponse({"errors": errors})

        # return redirect(reverse('edit-tearsheet', kwargs={'id': id}))

    else:
        return HttpResponse("Request method not supported")


@api_view(["POST"])
def create_caption_api(request, id):

    errors = None

    if request.method == "POST":

        order_no = len(FormulaImageCaption.objects.filter(tear_sheet_id=id))
        request.data["data"].update({"order_no": order_no + 1})

        FormulaImageCaption.objects.create(**request.data["data"])

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

        FormulaImageCaption.objects.filter(id=request.data["data"]["id"]).delete()

    else:

        FormulaImageCaption.objects.filter(id=request.data["data"]["id"]).update(
            **request.data["data"]
        )

    return JsonResponse({"errors": errors})


@api_view(["POST"])
def edit_footer_api(request):

    errors = None

    if request.data["data"]["name"] == "" and request.data["data"]["details"] == "":

        FormulaTearSheetFooterDetail.objects.filter(
            id=request.data["data"]["id"]
        ).delete()

    else:

        FormulaTearSheetFooterDetail.objects.filter(
            id=request.data["data"]["id"]
        ).update(**request.data["data"])

    return JsonResponse({"errors": errors})


@api_view(["POST"])
def create_footer_api(request, id):

    errors = None

    if request.method == "POST":

        order_no = len(FormulaTearSheetFooterDetail.objects.filter(tear_sheet_id=id))
        request.data["data"].update({"order": order_no + 1})
        FormulaTearSheetFooterDetail.objects.create(**request.data["data"])

        return JsonResponse({"errors": errors})

        # return redirect(reverse('edit-tearsheet', kwargs={'id': id}))

    else:
        return HttpResponse("Request method not supported")
