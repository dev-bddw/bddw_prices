from sqlite3 import IntegrityError

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse, redirect, render

from price_records.models import PriceRecord
from products.models import CatSeriesItem

from .helpers import return_details_by_title, return_price_records_by_rule_type
from .models import ImageCaption, TearSheet, TearSheetDetail, TearSheetFooterDetail


@login_required
def list_view(request):

    return render(
        request,
        "list_view.html",
        {
            "tearsheets": TearSheet.objects.all().order_by("-updated_on"),
        },
    )


@login_required
def print_all(request):

    # default_storage = get_storage_class()

    # tear_sheets = TearSheet.objects.all()

    # batch_name = str(random.randrange(1000000))

    # for tear_sheet in tear_sheets:

    #     url = settings.PDF_APP_URL + settings.SITE_URL + tear_sheet.get_printing_url()

    #     requests.get(url)

    #     file_obj = File(b"hi how are you", name=tear_sheet.get_slug_title() + ".pdf")

    #     # do your validation here e.g. file size/type check

    #     # organize a path for the file in bucket
    #     file_directory_within_bucket = "user_upload_files/{username}".format(
    #         username=request.user
    #     )

    #     # synthesize a full file path; note that we included the filename
    #     file_path_within_bucket = os.path.join(
    #         file_directory_within_bucket, file_obj.name
    #     )

    #     media_storage = default_storage()

    #     media_storage.save(file_path_within_bucket, file_obj)

    return HttpResponse("<p>ALL DONE</p>")

    # zip_path = os.path.join(settings.MEDIA_ROOT, "zip_files")

    # try:
    #     os.makedirs(zip_path, exist_ok=True)
    # except Exception:
    #     pass

    # archive = shutil.make_archive(
    #     zip_path + "/" + f"BDDW_PDFS_ALL-{batch_name}", "zip", folder_path
    # )

    # file_obj = default_storage.open(archive)

    # default_storage.save(
    #     os.path.join(settings.MEDIA_ROOT, f"zip_files/BDDW_PDFS_ALL-{batch_name}.zip"),
    #     file_obj,
    # )

    # return render(
    #     request,
    #     "zip_download.html",
    #     {"file_url": settings.MEDIA_URL + f"zip_files/BDDW_PDFS_ALL-{batch_name}.zip"},
    # )


def detail_view(request, pk):

    tear_sheet = TearSheet.objects.get(pk=pk)
    captions = ImageCaption.objects.filter(tear_sheet=tear_sheet)
    footer_details = TearSheetFooterDetail.objects.filter(tear_sheet=tear_sheet)

    return render(
        request,
        "detail_view.html",
        {
            "tearsheet": tear_sheet,
            "details": return_details_by_title(pk),
            "captions": captions,
            "footer_details": footer_details,
            "price_records": return_price_records_by_rule_type(pk),
        },
    )


@login_required
def edit_view(request, pk):

    tear_sheet = TearSheet.objects.get(pk=pk)
    details = TearSheetDetail.objects.filter(tear_sheet=tear_sheet)
    captions = ImageCaption.objects.filter(tear_sheet=tear_sheet)
    footer_details = TearSheetFooterDetail.objects.filter(tear_sheet=tear_sheet)

    cat_series_items = CatSeriesItem.objects.filter(
        tear_sheet=tear_sheet
    ).prefetch_related()

    # https://docs.djangoproject.com/en/4.0/ref/models/querysets/
    # this is how you return a list of foreign keys from a queryset of another model
    price_records = PriceRecord.objects.filter(cat_series_item__in=cat_series_items)

    return render(
        request,
        "edit_view.html",
        {
            "tearsheet": tear_sheet,
            "details": details,
            "captions": captions,
            "footer_details": footer_details,
            "price_records": price_records,
            "cat_series_items": cat_series_items,
        },
    )


@login_required
def change_template_hx(request, pk):

    tearsheet = TearSheet.objects.get(pk=pk)

    if request.method == "POST":
        tearsheet.template = request.POST.get("template")
        tearsheet.save()

    return render(request, "hx/post/edit/template.html", {"tearsheet": tearsheet})


@login_required
def change_title_hx(request, pk):

    tearsheet = TearSheet.objects.get(pk=pk)

    if request.method == "PUT":
        return render(request, "hx/post/edit/title.html", {"tearsheet": tearsheet})

    if request.method == "POST":
        tearsheet.title = request.POST.get("title")
        tearsheet.save()

        return render(request, "hx/post/edit/title.html", {"tearsheet": tearsheet})

    if request.method == "GET":
        return render(request, "hx/get/title.html", {"tearsheet": tearsheet})


@login_required
def change_image_hx(request, pk):

    tear_sheet = TearSheet.objects.get(pk=pk)

    if request.method == "POST":

        image = request.FILES.get("fileinput")
        tear_sheet.image = image
        tear_sheet.save()

        return redirect(tear_sheet.get_edit_url())

    else:
        pass


@login_required
def change_caption_hx(request, pk):

    caption = ImageCaption.objects.get(pk=pk)

    if request.method == "DELETE":
        caption.delete()
        return HttpResponse("")

    if request.method == "PUT":
        return render(request, "hx/post/edit/caption.html", {"caption": caption})

    if request.method == "POST":
        caption.caption_title = request.POST.get("title")
        caption.caption = request.POST.get("caption")
        caption.save()
        return render(request, "hx/post/edit/caption.html", {"caption": caption})

    if request.method == "GET":
        return render(request, "hx/get/caption.html", {"caption": caption})


@login_required
def change_detail_hx(request, pk):
    detail = TearSheetDetail.objects.get(pk=pk)

    if request.method == "DELETE":
        detail.delete()
        return HttpResponse("")

    if request.method == "PUT":

        return render(request, "hx/post/edit/detail.html", {"detail": detail})

    if request.method == "POST":
        detail.name = request.POST.get("name")
        detail.details = request.POST.get("details")
        detail.save()

        return render(request, "hx/post/edit/detail.html", {"detail": detail})

    if request.method == "GET":
        return render(request, "hx/get/detail.html", {"detail": detail})


@login_required
def change_price_record_hx(request, pk):
    price_record = PriceRecord.objects.get(pk=pk)

    if request.method == "DELETE":
        price_record.delete()
        return HttpResponse("")

    if request.method == "PUT":

        return render(
            request, "hx/post/edit/price_record.html", {"price_record": price_record}
        )

    if request.method == "POST":

        price_record.rule_type = request.POST.get("rule_type")
        price_record.rule_display_1 = request.POST.get("rule_display_1")
        price_record.rule_display_2 = request.POST.get("rule_display_2")
        price_record.list_price = request.POST.get("list_price")
        price_record.save()

        return render(
            request, "hx/post/edit/price_record.html", {"price_record": price_record}
        )

    if request.method == "GET":
        return render(
            request, "hx/get/price_record.html", {"price_record": price_record}
        )


@login_required
def change_footer_detail_hx(request, pk):
    footer_detail = TearSheetFooterDetail.objects.get(pk=pk)

    if request.method == "DELETE":
        footer_detail.delete()
        return HttpResponse("")

    if request.method == "PUT":

        return render(
            request, "hx/post/edit/footer_detail.html", {"footer_detail": footer_detail}
        )

    if request.method == "POST":
        footer_detail.name = request.POST.get("name")
        footer_detail.details = request.POST.get("details")
        footer_detail.save()

        return render(
            request, "hx/post/edit/footer_detail.html", {"footer_detail": footer_detail}
        )
    if request.method == "GET":
        return render(
            request, "hx/get/footer_detail.html", {"footer_detail": footer_detail}
        )


@login_required
def create_caption_hx(request, pk):

    if request.method == "POST":
        tear_sheet = TearSheet.objects.get(pk=pk)
        caption = ImageCaption.objects.create(
            caption_title=request.POST.get("title"),
            caption=request.POST.get("caption"),
            tear_sheet=tear_sheet,
            order_no=1
            + max(
                [x.order_no for x in ImageCaption.objects.filter(tear_sheet=tear_sheet)]
            )
            if [x.order_no for x in ImageCaption.objects.filter(tear_sheet=tear_sheet)]
            != []
            else 1,
        )

        return render(
            request,
            "hx/post/create/caption.html",
            {"caption": caption, "tearsheet": tear_sheet},
        )


@login_required
def create_detail_hx(request, pk):

    if request.method == "POST":
        tear_sheet = TearSheet.objects.get(pk=pk)
        detail = TearSheetDetail.objects.create(
            name=request.POST.get("name"),
            details=request.POST.get("details"),
            tear_sheet=tear_sheet,
            order=1
            + max(
                [x.order for x in TearSheetDetail.objects.filter(tear_sheet=tear_sheet)]
            )
            if [x.order for x in TearSheetDetail.objects.filter(tear_sheet=tear_sheet)]
            != []
            else 1,
        )

        return render(
            request,
            "hx/post/create/detail.html",
            {"detail": detail, "tearsheet": tear_sheet},
        )


@login_required
def create_price_record_hx(request):

    if request.method == "POST":
        csi = CatSeriesItem.objects.get(pk=request.POST.get("cat_series_item"))
        order = (
            1 + max([x.order for x in PriceRecord.objects.filter(cat_series_item=csi)])
            if [x.order for x in PriceRecord.objects.filter(cat_series_item=csi)] != []
            else 1
        )
        cat_series_items = CatSeriesItem.objects.filter(tear_sheet=csi.tear_sheet)
        try:
            price_record = PriceRecord.objects.create(
                rule_type=request.POST.get("rule_type"),
                rule_display_1=request.POST.get("rule_display_1"),
                rule_display_2=request.POST.get("rule_display_2"),
                list_price=request.POST.get("list_price"),
                cat_series_item=CatSeriesItem.objects.get(
                    pk=request.POST.get("cat_series_item")
                ),
                order=order,
            )
        except IntegrityError:
            pass

        return render(
            request,
            "hx/post/create/price_record.html",
            {"price_record": price_record, "cat_series_items": cat_series_items},
        )


@login_required
def create_footer_detail_hx(request, pk):
    if request.method == "POST":
        tear_sheet = TearSheet.objects.get(pk=pk)
        detail = TearSheetFooterDetail.objects.create(
            name=request.POST.get("name"),
            details=request.POST.get("details"),
            tear_sheet=tear_sheet,
            order=1
            + max(
                [
                    x.order
                    for x in TearSheetFooterDetail.objects.filter(tear_sheet=tear_sheet)
                ]
            )
            if [
                x.order
                for x in TearSheetFooterDetail.objects.filter(tear_sheet=tear_sheet)
            ]
            != []
            else 1,
        )

        return render(
            request,
            "hx/post/create/footer_detail.html",
            {"footer_detail": detail, "tearsheet": tear_sheet},
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
        "print_views/list_and_net.html",
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
        settings.PDF_APP_URL + settings.SITE_URL + tear_sheet.get_printing_url()
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
        settings.PDF_APP_URL + settings.SITE_URL + tear_sheet.get_printing_url_no_list()
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
        "print_views/list_only.html",
        {
            "tearsheet": tear_sheet,
            "details": return_details_by_title(pk),
            "captions": captions,
            "footer_details": footer_details,
            "price_records": return_price_records_by_rule_type(pk),
        },
    )
