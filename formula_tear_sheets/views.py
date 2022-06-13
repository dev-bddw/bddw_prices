from django.shortcuts import redirect, render

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
        "list_view.html",
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
            request, "formula_tear_sheets/hx/post/title.html", {"tearsheet": tearsheet}
        )

    if request.method == "POST":
        tearsheet.title = request.POST.get("title")
        tearsheet.save()

        return render(
            request, "formula_tear_sheets/hx/post/title.html", {"tearsheet": tearsheet}
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

    if request.method == "PUT":
        return render(
            request, "formula_tear_sheets/hx/post/caption.html", {"caption": caption}
        )

    if request.method == "POST":
        caption.caption_title = request.POST.get("title")
        caption.caption = request.POST.get("caption")
        caption.save()
        return render(
            request, "formula_tear_sheets/hx/post/caption.html", {"caption": caption}
        )

    if request.method == "GET":
        return render(
            request, "formula_tear_sheets/hx/get/caption.html", {"caption": caption}
        )


def change_detail_hx(request, pk):
    detail = FormulaTearSheetDetail.objects.get(pk=pk)

    if request.method == "PUT":

        return render(
            request, "formula_tear_sheets/hx/post/detail.html", {"detail": detail}
        )

    if request.method == "POST":
        detail.name = request.POST.get("name")
        detail.details = request.POST.get("details")
        detail.save()

        return render(
            request, "formula_tear_sheets/hx/post/detail.html", {"detail": detail}
        )

    if request.method == "GET":
        return render(
            request, "formula_tear_sheets/hx/get/detail.html", {"detail": detail}
        )


def change_price_record_hx(request, pk):
    price_record = FormulaPriceRecord.objects.get(pk=pk)

    if request.method == "PUT":

        return render(
            request,
            "formula_tear_sheets/hx/post/price_record.html",
            {"price_record": price_record},
        )

    if request.method == "POST":

        price_record.rule_type = request.POST.get("rule_type")
        price_record.rule_display_1 = request.POST.get("rule_display_1")
        price_record.rule_display_2 = request.POST.get("rule_display_2")
        price_record.save()

        return render(
            request,
            "formula_tear_sheets/hx/post/price_record.html",
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

    if request.method == "PUT":

        return render(
            request,
            "formula_tear_sheets/hx/post/footer_detail.html",
            {"footer_detail": footer_detail},
        )

    if request.method == "POST":
        footer_detail.name = request.POST.get("name")
        footer_detail.details = request.POST.get("details")
        footer_detail.save()

        return render(
            request,
            "formula_tear_sheets/hx/post/footer_detail.html",
            {"footer_detail": footer_detail},
        )
    if request.method == "GET":
        return render(
            request,
            "formula_tear_sheets/hx/get/footer_detail.html",
            {"footer_detail": footer_detail},
        )


def detail_view_for_printing(request, pk):

    tear_sheet = FormulaTearSheet.objects.get(pk=pk)
    captions = FormulaImageCaption.objects.filter(tear_sheet=tear_sheet)
    footer_details = FormulaTearSheetFooterDetail.objects.filter(tear_sheet=tear_sheet)

    return render(
        request,
        "formula_tear_sheets/detail_view_for_pdf.html",
        {
            "tearsheet": tear_sheet,
            "details": return_details_by_title(pk),
            "captions": captions,
            "footer_details": footer_details,
            "price_records": return_price_records_by_rule_type(pk),
        },
    )


def detail_view_to_pdf(request, pk):

    tear_sheet = FormulaTearSheet.objects.get(pk=pk)

    url_string = (
        "https://bddw-pdf-api.herokuapp.com/api/render?url=https://bddwsalestools.com"
    )

    url_string += tear_sheet.get_printing_url()

    return redirect(url_string)
