from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse, redirect, render

from price_records.models import FormulaPriceRecord
from products.models import CatSeriesItem

from .helpers import return_details_by_title, return_price_records_by_rule_type
from .models import (
    FormulaImageCaption,
    FormulaTearSheet,
    FormulaTearSheetDetail,
    FormulaTearSheetFooterDetail,
)


def list_view(request):

    return render(
        request,
        "formula_tear_sheets/list_view.html",
        {
            "tearsheets": FormulaTearSheet.objects.all(),
        },
    )


def detail_view(request, pk):

    tear_sheet = FormulaTearSheet.objects.get(pk=pk)
    captions = FormulaImageCaption.objects.filter(tear_sheet=tear_sheet)
    footer_details = FormulaTearSheetFooterDetail.objects.filter(tear_sheet=tear_sheet)

    return render(
        request,
        "formula_tear_sheets/detail_view.html",
        {
            "tearsheet": tear_sheet,
            "details": return_details_by_title(pk),
            "captions": captions,
            "footer_details": footer_details,
            "price_records": return_price_records_by_rule_type(pk),
        },
    )


def edit_view(request, pk):

    tear_sheet = FormulaTearSheet.objects.get(pk=pk)
    details = FormulaTearSheetDetail.objects.filter(tear_sheet=tear_sheet)
    captions = FormulaImageCaption.objects.filter(tear_sheet=tear_sheet)
    footer_details = FormulaTearSheetFooterDetail.objects.filter(tear_sheet=tear_sheet)

    cat_series_items = CatSeriesItem.objects.filter(
        formula_tear_sheet=tear_sheet
    ).prefetch_related()

    # https://docs.djangoproject.com/en/4.0/ref/models/querysets/
    # this is how you return a list of foreign keys from a queryset of another model
    price_records = FormulaPriceRecord.objects.filter(
        cat_series_item__in=cat_series_items
    )

    return render(
        request,
        "formula_tear_sheets/edit_view.html",
        {
            "tearsheet": tear_sheet,
            "details": details,
            "captions": captions,
            "footer_details": footer_details,
            "price_records": price_records,
        },
    )


def change_title_hx(request, pk):

    tearsheet = FormulaTearSheet.objects.get(pk=pk)

    if request.method == "PUT":
        return render(
            request,
            "formula_tear_sheets/hx/post/edit/title.html",
            {"tearsheet": tearsheet},
        )

    if request.method == "POST":
        tearsheet.title = request.POST.get("title")
        tearsheet.save()

        return render(
            request,
            "formula_tear_sheets/hx/post/edit/title.html",
            {"tearsheet": tearsheet},
        )

    if request.method == "GET":
        return render(
            request, "formula_tear_sheets/hx/get/title.html", {"tearsheet": tearsheet}
        )


def change_image_hx(request, pk):

    tear_sheet = FormulaTearSheet.objects.get(pk=pk)

    if request.method == "POST":

        image = request.FILES.get("fileinput")
        tear_sheet.image = image
        tear_sheet.save()

        return redirect(tear_sheet.get_edit_url())

    else:
        pass


def change_caption_hx(request, pk):

    caption = FormulaImageCaption.objects.get(pk=pk)

    if request.method == "DELETE":
        caption.delete()

        return HttpResponse("")

    if request.method == "PUT":
        return render(
            request,
            "formula_tear_sheets/hx/post/edit/caption.html",
            {"caption": caption},
        )

    if request.method == "POST":
        caption.caption_title = request.POST.get("title")
        caption.caption = request.POST.get("caption")
        caption.save()
        return render(
            request,
            "formula_tear_sheets/hx/post/edit/caption.html",
            {"caption": caption},
        )

    if request.method == "GET":
        return render(
            request, "formula_tear_sheets/hx/get/caption.html", {"caption": caption}
        )


def change_detail_hx(request, pk):
    detail = FormulaTearSheetDetail.objects.get(pk=pk)

    if request.method == "DELETE":
        detail.delete()
        return HttpResponse("")

    if request.method == "PUT":

        return render(
            request, "formula_tear_sheets/hx/post/edit/detail.html", {"detail": detail}
        )

    if request.method == "POST":
        detail.name = request.POST.get("name")
        detail.details = request.POST.get("details")
        detail.save()

        return render(
            request, "formula_tear_sheets/hx/post/edit/detail.html", {"detail": detail}
        )

    if request.method == "GET":
        return render(
            request, "formula_tear_sheets/hx/get/detail.html", {"detail": detail}
        )


def change_price_record_hx(request, pk):
    price_record = FormulaPriceRecord.objects.get(pk=pk)

    if request.method == "DELETE":
        price_record.delete()

        return HttpResponse("")

    if request.method == "PUT":

        return render(
            request,
            "formula_tear_sheets/hx/post/edit/price_record.html",
            {"price_record": price_record},
        )

    if request.method == "POST":

        price_record.rule_type = request.POST.get("rule_type")
        price_record.rule_display_1 = request.POST.get("rule_display_1")
        price_record.rule_display_2 = request.POST.get("rule_display_2")
        price_record.save()

        return render(
            request,
            "formula_tear_sheets/hx/post/edit/price_record.html",
            {"price_record": price_record},
        )

    if request.method == "GET":
        return render(
            request,
            "formula_tear_sheets/hx/get/price_record.html",
            {"price_record": price_record},
        )


def change_footer_detail_hx(request, pk):
    footer_detail = FormulaTearSheetFooterDetail.objects.get(pk=pk)

    if request.method == "DELETE":
        footer_detail.delete()

        return HttpResponse("")

    if request.method == "PUT":

        return render(
            request,
            "formula_tear_sheets/hx/post/edit/footer_detail.html",
            {"footer_detail": footer_detail},
        )

    if request.method == "POST":
        footer_detail.name = request.POST.get("name")
        footer_detail.details = request.POST.get("details")
        footer_detail.save()

        return render(
            request,
            "formula_tear_sheets/hx/post/edit/footer_detail.html",
            {"footer_detail": footer_detail},
        )
    if request.method == "GET":
        return render(
            request,
            "formula_tear_sheets/hx/get/footer_detail.html",
            {"footer_detail": footer_detail},
        )


@login_required
def create_caption_hx(request, pk):

    if request.method == "POST":
        tear_sheet = FormulaTearSheet.objects.get(pk=pk)
        caption = FormulaImageCaption.objects.create(
            caption_title=request.POST.get("title"),
            caption=request.POST.get("caption"),
            tear_sheet=tear_sheet,
            order_no=1
            + max(
                [
                    x.order_no
                    for x in FormulaImageCaption.objects.filter(tear_sheet=tear_sheet)
                ]
            )
            if [
                x.order_no
                for x in FormulaImageCaption.objects.filter(tear_sheet=tear_sheet)
            ]
            != []
            else 1,
        )

        return render(
            request,
            "formula_tear_sheets/hx/post/create/caption.html",
            {"caption": caption, "tearsheet": tear_sheet},
        )


@login_required
def create_detail_hx(request, pk):

    if request.method == "POST":
        tear_sheet = FormulaTearSheet.objects.get(pk=pk)
        detail = FormulaTearSheetDetail.objects.create(
            name=request.POST.get("name"),
            details=request.POST.get("details"),
            tear_sheet=tear_sheet,
            order=1
            + max(
                [
                    x.order
                    for x in FormulaTearSheetDetail.objects.filter(
                        tear_sheet=tear_sheet
                    )
                ]
            )
            if [
                x.order
                for x in FormulaTearSheetDetail.objects.filter(tear_sheet=tear_sheet)
            ]
            != []
            else 1,
        )

        return render(
            request,
            "formula_tear_sheets/hx/post/create/detail.html",
            {"detail": detail, "tearsheet": tear_sheet},
        )


@login_required
def create_footer_detail_hx(request, pk):
    if request.method == "POST":
        tear_sheet = FormulaTearSheet.objects.get(pk=pk)
        detail = FormulaTearSheetFooterDetail.objects.create(
            name=request.POST.get("name"),
            details=request.POST.get("details"),
            tear_sheet=tear_sheet,
            order=1
            + max(
                [
                    x.order
                    for x in FormulaTearSheetFooterDetail.objects.filter(
                        tear_sheet=tear_sheet
                    )
                ]
            )
            if [
                x.order
                for x in FormulaTearSheetFooterDetail.objects.filter(
                    tear_sheet=tear_sheet
                )
            ]
            != []
            else 1,
        )

        return render(
            request,
            "formula_tear_sheets/hx/post/create/footer_detail.html",
            {"footer_detail": detail, "tearsheet": tear_sheet},
        )


@login_required
def change_template_hx(request, pk):

    tearsheet = FormulaTearSheet.objects.get(pk=pk)

    if request.method == "POST":
        tearsheet.template = request.POST.get("template")
        tearsheet.save()

    return render(
        request,
        "formula_tear_sheets/hx/post/edit/template.html",
        {"tearsheet": tearsheet},
    )


def detail_view_for_printing(request, pk):

    number_of = 0

    tear_sheet = FormulaTearSheet.objects.get(pk=pk)
    captions = FormulaImageCaption.objects.filter(tear_sheet=tear_sheet)
    footer_details = FormulaTearSheetFooterDetail.objects.filter(tear_sheet=tear_sheet)

    # spacing size b/t records and footer
    # we should actually perform a rational calculation here that
    # includes getting the tearsheet.img.height value and sbtrcts

    number_of += len(captions) + len(footer_details)

    return render(
        request,
        "formula_tear_sheets/print_views/list_and_net.html",
        {
            "tearsheet": tear_sheet,
            "details": return_details_by_title(pk),
            "captions": captions,
            "footer_details": footer_details,
            "price_records": return_price_records_by_rule_type(pk),
        },
    )


def redirect_detail_view_to_pdf(request, pk):
    tear_sheet = FormulaTearSheet.objects.get(pk=pk)

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

    tear_sheet = FormulaTearSheet.objects.get(pk=pk)

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

    tear_sheet = FormulaTearSheet.objects.get(pk=pk)
    captions = FormulaImageCaption.objects.filter(tear_sheet=tear_sheet)
    footer_details = FormulaTearSheetFooterDetail.objects.filter(tear_sheet=tear_sheet)

    return render(
        request,
        "formula_tear_sheets/print_views/list_only.html",
        {
            "tearsheet": tear_sheet,
            "details": return_details_by_title(pk),
            "captions": captions,
            "footer_details": footer_details,
            "price_records": return_price_records_by_rule_type(pk),
        },
    )
