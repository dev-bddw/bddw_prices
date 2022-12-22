import os
import random
import zipfile
from io import BytesIO

import boto3
import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse, redirect, render

from tear_sheets.models import ImageCaption, TearSheet, TearSheetFooterDetail

from .helpers import return_details_by_title, return_price_records_by_rule_type


@login_required
def list_view(request):

    return render(
        request,
        "gbp_list_view.html",
        {
            "tearsheets": TearSheet.objects.all().order_by("-updated_on"),
        },
    )


@login_required
def print_all(request):

    s3 = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )

    batch_name = str(random.randrange(1000000))
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    object_dir = f'/var/tmp/{batch_name}/'
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

        pdf_file_name = f"{tear_sheet.get_slug_title().upper()}-GBP-TEAR-SHEET.pdf"

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

        pdf_file_name = f"{tear_sheet.get_slug_title().upper()}-GBP-NET.pdf"

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
        + f"GBP-TEARSHEET-ARCHIVE-{batch_name}.zip"
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


@login_required
def detail_view(request, pk):

    tear_sheet = TearSheet.objects.get(pk=pk)
    captions = ImageCaption.objects.filter(tear_sheet=tear_sheet)
    footer_details = TearSheetFooterDetail.objects.filter(tear_sheet=tear_sheet)

    return render(
        request,
        "gbp_detail_view.html",
        {
            "tearsheet": tear_sheet,
            "details": return_details_by_title(pk),
            "captions": captions,
            "footer_details": footer_details,
            "price_records": return_price_records_by_rule_type(pk),
        },
    )


def detail_view_for_printing(request, pk):

    number_of = 0

    tear_sheet = TearSheet.objects.get(pk=pk)
    captions = ImageCaption.objects.filter(tear_sheet=tear_sheet)
    footer_details = TearSheetFooterDetail.objects.filter(tear_sheet=tear_sheet)

    # spacing size b/t records and footer
    # we should actually perform a rational calculation here that
    # includes getting the tearsheet.img.height value and sbtrcts

    number_of += len(captions) + len(footer_details)

    return render(
        request,
        "gbp_print_views/list_and_trade.html",
        {
            "tearsheet": tear_sheet,
            "details": return_details_by_title(pk),
            "captions": captions,
            "footer_details": footer_details,
            "price_records": return_price_records_by_rule_type(pk),
        },
    )


def redirect_detail_view_to_pdf(request, pk):
    tear_sheet = TearSheet.objects.get(pk=pk)

    url_string = (
        settings.PDF_APP_URL + settings.SITE_URL + tear_sheet.get_gbp_printing_url()
    )

    parameter = (
        f"&attachmentName={tear_sheet.get_slug_title().upper()}-NET.pdf"
        if request.GET.get("justDownload") == "True"
        else ""
    )

    url_string += parameter

    return redirect(url_string)


def redirect_detail_view_to_pdf_list(request, pk):

    tear_sheet = TearSheet.objects.get(pk=pk)

    url_string = (
        settings.PDF_APP_URL + settings.SITE_URL + tear_sheet.get_gbp_printing_url_no_list()
    )

    parameter = (
        f"&attachmentName={tear_sheet.get_slug_title().upper()}-TEAR-SHEET.pdf"
        if request.GET.get("justDownload") == "True"
        else ""
    )

    url_string += parameter

    print(url_string)

    return redirect(url_string)


def detail_view_for_printing_list(request, pk):

    tear_sheet = TearSheet.objects.get(pk=pk)
    captions = ImageCaption.objects.filter(tear_sheet=tear_sheet)
    footer_details = TearSheetFooterDetail.objects.filter(tear_sheet=tear_sheet)

    return render(
        request,
        "gbp_print_views/list_only.html",
        {
            "tearsheet": tear_sheet,
            "details": return_details_by_title(pk),
            "captions": captions,
            "footer_details": footer_details,
            "price_records": return_price_records_by_rule_type(pk),
        },
    )
