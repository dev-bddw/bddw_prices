import json
import os
import random
import zipfile
from io import BytesIO

import boto3
import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import HttpResponse, redirect, render
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view

from formula_tear_sheets.models import (
    FormulaImageCaption,
    FormulaTearSheet,
    FormulaTearSheetDetail,
    FormulaTearSheetFooterDetail,
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

        x = FormulaTearSheet.objects.get(id=id)

        context = {
            "auth_token": token.key,
            "tearsheet": {
                "id": id,
                "title": x.title,
                "sdata": x.sdata,
                "template": x.template,
                "img": x.image.url,
                "price_records": return_price_records_by_rule_type(id)
                if return_price_records_by_rule_type(id) is not None
                else [],
                "captions": [
                    {"id": c.id, "caption_title": c.caption_title, "caption": c.caption}
                    for c in FormulaImageCaption.objects.filter(tear_sheet_id=id)
                ]
                if FormulaImageCaption.objects.filter(tear_sheet_id=id) is not None
                else [],
                "details": return_details_by_title(id)
                if return_details_by_title(id) is not None
                else [],
                "footer_details": [
                    {"id": f.id, "name": f.name, "details": f.details}
                    for f in FormulaTearSheetFooterDetail.objects.filter(
                        tear_sheet_id=id
                    )
                ]
                if FormulaTearSheetFooterDetail.objects.filter(tear_sheet_id=id)
                is not None
                else [],
            },
        }

        context = json.dumps(context)

        return render(
            request, "form_detail/dist/index.html", {"id": id, "context": context}
        )


@login_required
def edit_view_entry(request, id):
    user = request.user

    try:
        token = Token.objects.get(user=user)
    except Token.DoesNotExist:
        token = Token.objects.create(user=user)

    if request.method == "GET":

        x = FormulaTearSheet.objects.get(id=id)

        context = {
            "auth_token": token.key,
            "tearsheet": {
                "id": id,
                "title": x.title,
                "sdata": x.sdata,
                "template": x.template,
                "img": x.image.url,
                "price_records": return_price_records_by_rule_type(id)
                if return_price_records_by_rule_type(id) is not None
                else [],
                "captions": [
                    {"id": c.id, "caption_title": c.caption_title, "caption": c.caption}
                    for c in FormulaImageCaption.objects.filter(tear_sheet_id=id)
                ]
                if FormulaImageCaption.objects.filter(tear_sheet_id=id) is not None
                else [],
                "details": return_details_by_title(id)
                if return_details_by_title(id) is not None
                else [],
                "footer_details": [
                    {"id": f.id, "name": f.name, "details": f.details}
                    for f in FormulaTearSheetFooterDetail.objects.filter(
                        tear_sheet_id=id
                    )
                ]
                if FormulaTearSheetFooterDetail.objects.filter(tear_sheet_id=id)
                is not None
                else [],
            },
        }

        context = json.dumps(context)

        return render(
            request, "form_edit/dist/index.html", {"id": id, "context": context}
        )


@api_view(["POST"])
def edit_tearsheet_api(request, id):

    if request.method == "POST":

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


@login_required
def print_all(request):
    """
    returns a link to rar file of all tearsheets
    """
    s3 = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )

    batch_name = str(random.randrange(1000000))
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    object_dir = f"/var/tmp/{batch_name}/"
    pdf_list = []

    # make local directory to place pdf files

    os.makedirs(object_dir)

    # save all the pdfs from the heroku api & load path / bytes into a list of tuples
    for tear_sheet in FormulaTearSheet.objects.all():
        url_string = (
            settings.PDF_APP_URL
            + settings.SITE_URL
            + tear_sheet.get_printing_url_no_list()
        )

        pdf_file_name = f"{tear_sheet.get_slug_title().upper()}-TEAR-SHEET.pdf"

        parameter = f"&attachmentName={pdf_file_name}"

        url_string += parameter

        response = requests.get(url_string)

        bytes_container = BytesIO(response.content)

        # if we wanted to save the pdfs locally but we don't need to
        # because we have the byte data
        # object_path = object_dir + pdf_file_name
        # with open(object_path, "wb") as pdf_file:
        #     pdf_file.write(bytes_container.getvalue())

        pdf_list.append((pdf_file_name, bytes_container))

    for tear_sheet in FormulaTearSheet.objects.all():
        url_string = (
            settings.PDF_APP_URL + settings.SITE_URL + tear_sheet.get_printing_url()
        )

        pdf_file_name = f"{tear_sheet.get_slug_title().upper()}-NET.pdf"

        parameter = f"&attachmentName={pdf_file_name}"

        url_string += parameter

        response = requests.get(url_string)

        bytes_container = BytesIO(response.content)

        # if we wanted to save the pfs locally but we don't need to
        # because we have the byte data
        # object_path = object_dir + pdf_file_name
        # with open(object_path, "wb") as pdf_file:
        #     pdf_file.write(bytes_container.getvalue())

        pdf_list.append((pdf_file_name, bytes_container))

    archive = BytesIO()
    s3_path = (
        f"media/tearsheet-batch-print/{batch_name}/"
        + f"TEARSHEET-ARCHIVE-{batch_name}.zip"
    )

    # process tuples into the zip archive buffer

    with zipfile.ZipFile(archive, "w") as zip_archive:

        for path, data in pdf_list:

            file = zipfile.ZipInfo(path)
            zip_archive.writestr(file, data.getvalue())

    # save the buffer to a real file

    with open(object_dir + "all-tearsheets.zip", "wb") as f:
        f.write(archive.getbuffer())

    archive.close()

    # upload the file to s3

    s3.upload_file(object_dir + "all-tearsheets.zip", bucket_name, s3_path)

    return HttpResponse(
        f"<a href='{settings.MEDIA_URL}"
        + f"tearsheet-batch-print/{batch_name}/TEARSHEET-ARCHIVE-{batch_name}.zip'>download</a>"
    )


def detail_view_for_printing(request, id):
    """
    the view the printer app uses to create pdfs
    """
    if request.method == "GET":

        x = FormulaTearSheet.objects.get(id=id)

        context = {
            "auth_token": None,
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
                    for c in FormulaImageCaption.objects.filter(tear_sheet_id=id)
                ]
                if FormulaImageCaption.objects.filter(tear_sheet_id=id) is not None
                else [],
                "details": return_details_by_title(id)
                if return_details_by_title(id) is not None
                else [],
                "footer_details": [
                    {"id": f.id, "name": f.name, "details": f.details}
                    for f in FormulaTearSheetFooterDetail.objects.filter(
                        tear_sheet_id=id
                    )
                ]
                if FormulaTearSheetFooterDetail.objects.filter(tear_sheet_id=id)
                is not None
                else [],
            },
        }

        context = json.dumps(context)

        return render(
            request,
            "form_detail_for_print/dist/index.html",
            {"id": id, "context": context},
        )


def detail_view_for_printing_list(request, id):
    """
    detail view pdf app uses to create list pdfs
    """
    if request.method == "GET":

        x = FormulaTearSheet.objects.get(id=id)

        context = {
            "auth_token": None,
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
                    for c in FormulaImageCaption.objects.filter(tear_sheet_id=id)
                ]
                if FormulaImageCaption.objects.filter(tear_sheet_id=id) is not None
                else [],
                "details": return_details_by_title(id)
                if return_details_by_title(id) is not None
                else [],
                "footer_details": [
                    {"id": f.id, "name": f.name, "details": f.details}
                    for f in FormulaTearSheetFooterDetail.objects.filter(
                        tear_sheet_id=id
                    )
                ]
                if FormulaTearSheetFooterDetail.objects.filter(tear_sheet_id=id)
                is not None
                else [],
            },
        }

        context = json.dumps(context)

        return render(
            request,
            "form_detail_for_print_list/dist/index.html",
            {"id": id, "context": context},
        )


def redirect_detail_view_to_pdf(request, id):
    """
    redirect to the proper url for the printer
    """
    tear_sheet = FormulaTearSheet.objects.get(pk=id)

    url_string = (
        settings.PDF_APP_URL + settings.SITE_URL + tear_sheet.get_printing_url()
    )

    parameter = (
        f"&attachmentName={tear_sheet.get_slug_title().upper()}-NET.pdf"
        if request.GET.get("justDownload") == "True"
        else ""
    )

    url_string += parameter

    return redirect(url_string)


def redirect_detail_view_to_pdf_list(request, id):
    """
    redirect to the proper url for the printer
    """

    tear_sheet = FormulaTearSheet.objects.get(id=id)

    url_string = (
        settings.PDF_APP_URL + settings.SITE_URL + tear_sheet.get_printing_url_no_list()
    )

    parameter = (
        f"&attachmentName={tear_sheet.get_slug_title().upper()}-TEAR-SHEET.pdf"
        if request.GET.get("justDownload") == "True"
        else ""
    )

    url_string += parameter

    return redirect(url_string)
