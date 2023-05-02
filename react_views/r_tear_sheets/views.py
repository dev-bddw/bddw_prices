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

from price_records.models import PriceRecord
from tear_sheets.models import (
    ImageCaption,
    TearSheet,
    TearSheetDetail,
    TearSheetFooterDetail,
)

from .helpers import return_details_by_title, return_price_records_by_rule_type


def detail_view_entry(request, id):
    user = request.user

#        token = Token.objects.get(user=user)
#    except Token.DoesNotExist:
#        token = Token.objects.create(user=user)

    if request.method == "GET":

        x = TearSheet.objects.get(id=id)

        context = {
            "auth_token": 'fc02c4f9cf69a674b0a7d9b69b0be4b9fc99aa31',
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
    for tear_sheet in TearSheet.objects.all():
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

    for tear_sheet in TearSheet.objects.all():
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

        x = TearSheet.objects.get(id=id)

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

        return render(
            request, "detail_for_print/dist/index.html", {"id": id, "context": context}
        )


def detail_view_for_printing_list(request, id):
    """
    detail view pdf app uses to create list pdfs
    """
    if request.method == "GET":

        x = TearSheet.objects.get(id=id)

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

        return render(
            request,
            "detail_for_print_list/dist/index.html",
            {"id": id, "context": context},
        )


def redirect_detail_view_to_pdf(request, id):
    """
    redirect to the proper url for the printer
    """
    tear_sheet = TearSheet.objects.get(pk=id)

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

    tear_sheet = TearSheet.objects.get(id=id)

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

def render_pdf(request, id):

    from django.template import Context, Template
    from django.template.loader import get_template
    

    user = request.user
    try:
        token = Token.objects.get(user=user)
    except Token.DoesNotExist:
        token = Token.objects.create(user=user)


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

    context_ = {"id": id, "context": context}
    template = get_template("detail/dist/index.html")
    _html = template.render(context_)

    import requests
    
    headers = {'Content-Type': 'application/json'}

    response = requests.post(url=settings.PDF_APP_URL, headers=headers, json={'html': _html})
    
    return HttpResponse(response)

def test(request):

    return render(request, 'test/dist/index.html')
