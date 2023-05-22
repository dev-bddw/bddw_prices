import os
import random
import zipfile
from io import BytesIO

import boto3
import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse, redirect, render

from formula_tear_sheets.models import FormulaTearSheet

from .helpers import return_context


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

        context = return_context(request, id)

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

        context = return_context(request, id)

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
