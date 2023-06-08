import os
import random
import zipfile
from io import BytesIO

import boto3
import requests
from django.conf import settings

from formula_tear_sheets.models import FormulaTearSheet
from tear_sheets.models import TearSheet


def process_tearsheet(tearsheet):
    """
    returns lists of tuples with pdf information
    for tearsheet type, for tearsheet version (trade/net/etc)
    each type of tearsheet has two version
    i'm only like half aware of how this actually works -- I think the pdfs
    are actually never saved until it comes time to zip them, until then they live in memory,
    in a tuple with ( 'file name', bytes container'), then they are zipped, loaded into s3
    """
    # TEARSHEETS #
    # TEARSHEETS #
    # TEARSHEETS #
    if tearsheet["type"] == "tearsheet":
        # TEARSHEETS #
        # TEARSHEETS #
        # TEARSHEETS #

        tear_sheet = TearSheet.objects.get(id=tearsheet["id"])

        # PRINT NET AND LIST

        def return_url_tearsheet():
            """
            get the full url for the printer
            """
            return (
                settings.PDF_APP_URL
                + settings.SITE_URL
                + tear_sheet.get_printing_url()
                + f"&attachmentName={tear_sheet.get_slug_title().upper()}-NET.pdf"
            )

        def return_file_name_tearsheet():
            """
            get the full filename for tearsheet pdf
            """
            return f"{tear_sheet.get_slug_title().upper()}-NET.pdf"

        def package():
            response = requests.get(
                return_url_tearsheet()
            )  # make the request for the pdf
            bytes_container = BytesIO(response.content)  # store the pdf in a container
            return (
                return_file_name_tearsheet(),
                bytes_container,
            )  # add the name and reference to the list

        # PRINT LIST ONLY

        def return_url_tearsheet_no_list():
            """
            get the full url for the printer
            """
            return (
                settings.PDF_APP_URL
                + settings.SITE_URL
                + tear_sheet.get_printing_url_no_list()
                + f"&attachmentName={tear_sheet.get_slug_title().upper()}-TEAR-SHEET.pdf"
            )

        def return_file_name_tearsheet_no_list():
            """
            get the full filename for tearsheet pdf
            """
            return f"{tear_sheet.get_slug_title().upper()}-TEAR-SHEET.pdf"

        def package_no_list():
            """
            make the request to the url and
            save response content
            and store reference in tuples
            """
            response = requests.get(
                return_url_tearsheet_no_list()
            )  # make the request for the pdf
            bytes_container = BytesIO(response.content)  # store the pdf in a container
            return (
                return_file_name_tearsheet_no_list(),
                bytes_container,
            )  # add the name and reference to the list

        def return_complete_package():
            """
            add both tuples to a list
            """
            tuple_list = []
            tuple_list.append(package())
            tuple_list.append(package_no_list())

            return tuple_list

        print("package tearsheet success")
        return return_complete_package()

    # GBP TEARSHEETS #
    # GBP TEARSHEETS #
    # GBP TEARSHEETS #
    if tearsheet["type"] == "gbp":
        # GBP TEARSHEETS #
        # GBP TEARSHEETS #
        # GBP TEARSHEETS #

        tear_sheet = TearSheet.objects.get(id=tearsheet["id"])

        # PRINT TRADE AND LIST

        def return_url_gbp_tearsheet():
            """
            get the full url for the printer
            """
            return (
                settings.PDF_APP_URL
                + settings.SITE_URL
                + tear_sheet.get_gbp_printing_url()
                + f"&attachmentName={tear_sheet.get_slug_title().upper()}-GBP-TRADE.pdf"
            )

        def return_file_name_gbp_tearsheet():
            """
            get the full filename for tearsheet pdf
            """
            return f"{tear_sheet.get_slug_title().upper()}-GBP-TRADE.pdf"

        def package_gbp():
            response = requests.get(
                return_url_gbp_tearsheet()
            )  # make the request for the pdf
            bytes_container = BytesIO(response.content)  # store the pdf in a container
            return (
                return_file_name_gbp_tearsheet(),
                bytes_container,
            )  # add the name and reference to the list

        # PRINT LIST ONLY

        def return_url_gbp_tearsheet_no_list():
            """
            get the full url for the printer
            """
            return (
                settings.PDF_APP_URL
                + settings.SITE_URL
                + tear_sheet.get_gbp_printing_url_no_list()
                + f"&attachmentName={tear_sheet.get_slug_title().upper()}-GBP-TEAR-SHEET.pdf"
            )

        def return_file_name_gbp_tearsheet_no_list():
            """
            get the full filename for tearsheet pdf
            """
            return f"{tear_sheet.get_slug_title().upper()}-GBP-TEAR-SHEET.pdf"

        def package_gbp_no_list():
            """
            make the request to the url and
            save response content
            and store reference in tuples
            """
            response = requests.get(
                return_url_gbp_tearsheet_no_list()
            )  # make the request for the pdf
            bytes_container = BytesIO(response.content)  # store the pdf in a container
            return (
                return_file_name_gbp_tearsheet_no_list(),
                bytes_container,
            )  # add the name and reference to the list

        def return_complete_gbp_package():
            """
            add both tuples to a list
            """
            tuple_list = []
            tuple_list.append(package_gbp())
            tuple_list.append(package_gbp_no_list())

            return tuple_list

        print("package gbp success")
        return return_complete_gbp_package()

    # TEARSHEETS #
    # TEARSHEETS #
    # TEARSHEETS #
    if tearsheet["type"] == "formula":
        # TEARSHEETS #
        # TEARSHEETS #
        # TEARSHEETS #

        tear_sheet = FormulaTearSheet.objects.get(id=tearsheet["id"])

        # PRINT NET AND LIST

        def return_url_formula_tearsheet():
            """
            get the full url for the printer
            """
            return (
                settings.PDF_APP_URL
                + settings.SITE_URL
                + tear_sheet.get_printing_url()
                + f"&attachmentName={tear_sheet.get_slug_title().upper()}-NET.pdf"
            )

        def return_file_name_formula_tearsheet():
            """
            get the full filename for tearsheet pdf
            """
            return f"{tear_sheet.get_slug_title().upper()}-NET.pdf"

        def formula_package():
            response = requests.get(
                return_url_formula_tearsheet()
            )  # make the request for the pdf
            bytes_container = BytesIO(response.content)  # store the pdf in a container
            return (
                return_file_name_formula_tearsheet(),
                bytes_container,
            )  # add the name and reference to the list

        # PRINT LIST ONLY

        def return_url_formula_tearsheet_no_list():
            """
            get the full url for the printer
            """
            return (
                settings.PDF_APP_URL
                + settings.SITE_URL
                + tear_sheet.get_printing_url_no_list()
                + f"&attachmentName={tear_sheet.get_slug_title().upper()}-TEAR-SHEET.pdf"
            )

        def return_file_name_formula_tearsheet_no_list():
            """
            get the full filename for tearsheet pdf
            """
            return f"{tear_sheet.get_slug_title().upper()}-TEAR-SHEET.pdf"

        def package_formula_no_list():
            """
            make the request to the url and
            save response content
            and store reference in tuples
            """
            response = requests.get(
                return_url_formula_tearsheet_no_list()
            )  # make the request for the pdf
            bytes_container = BytesIO(response.content)  # store the pdf in a container
            return (
                return_file_name_formula_tearsheet_no_list(),
                bytes_container,
            )  # add the name and reference to the list

        def return_complete_formula_package():
            """
            add both tuples to a list
            """
            tuple_list = []
            tuple_list.append(formula_package())
            tuple_list.append(package_formula_no_list())

            return tuple_list

        print("package formula tearsheet success")
        return return_complete_formula_package()

    # GBP FORMULA #
    # GBP FORMULA #
    # GBP FORMULA #
    if tearsheet["type"] == "formula gbp":
        # GBP FORMULA #
        # GBP FORMULA #
        # GBP FORMULA #
        # GBP FORMULA #

        tear_sheet = FormulaTearSheet.objects.get(id=tearsheet["id"])

        # PRINT TRADE AND LIST

        def return_url_form_gbp_tearsheet():
            """
            get the full url for the printer
            """
            return (
                settings.PDF_APP_URL
                + settings.SITE_URL
                + tear_sheet.get_gbp_printing_url()
                + f"&attachmentName={tear_sheet.get_slug_title().upper()}-GBP-TRADE.pdf"
            )

        def return_file_name_form_gbp_tearsheet():
            """
            get the full filename for tearsheet pdf
            """
            return f"{tear_sheet.get_slug_title().upper()}-GBP-TRADE.pdf"

        def package_form_gbp():
            response = requests.get(
                return_url_form_gbp_tearsheet()
            )  # make the request for the pdf
            bytes_container = BytesIO(response.content)  # store the pdf in a container
            return (
                return_file_name_form_gbp_tearsheet(),
                bytes_container,
            )  # add the name and reference to the list

        # PRINT LIST ONLY

        def return_url_form_gbp_tearsheet_no_list():
            """
            get the full url for the printer
            """
            return (
                settings.PDF_APP_URL
                + settings.SITE_URL
                + tear_sheet.get_gbp_printing_url_no_list()
                + f"&attachmentName={tear_sheet.get_slug_title().upper()}-GBP-TEAR-SHEET.pdf"
            )

        def return_file_name_form_gbp_tearsheet_no_list():
            """
            get the full filename for tearsheet pdf
            """
            return f"{tear_sheet.get_slug_title().upper()}-GBP-TEAR-SHEET.pdf"

        def package_form_gbp_no_list():
            """
            make the request to the url and
            save response content
            and store reference in tuples
            """
            response = requests.get(
                return_url_form_gbp_tearsheet_no_list()
            )  # make the request for the pdf
            bytes_container = BytesIO(response.content)  # store the pdf in a container
            return (
                return_file_name_form_gbp_tearsheet_no_list(),
                bytes_container,
            )  # add the name and reference to the list

        def return_complete_form_gbp_package():
            """
            add both tuples to a list
            """
            tuple_list = []
            tuple_list.append(package_form_gbp())
            tuple_list.append(package_form_gbp_no_list())

            return tuple_list

        print("package form gbp success")
        return return_complete_form_gbp_package()

    else:

        return []


def print_tearsheets(tearsheets):
    """
    handles the printing and raring of a list of pdfs that come from the frontend
    """
    pdf_list = []
    s3 = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )

    batch_name = str(random.randrange(1000000))
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    object_dir = f"/var/tmp/{batch_name}/"

    # make local directory to place rar

    os.makedirs(object_dir)

    # process the tearsheet data into pdfs and pdf refrences
    for tearsheet in tearsheets:

        pdf_list += process_tearsheet(tearsheet)  # returns list of tuples

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

    return (
        f"{settings.MEDIA_URL}"
        + f"tearsheet-batch-print/{batch_name}/TEARSHEET-ARCHIVE-{batch_name}.zip"
    )
