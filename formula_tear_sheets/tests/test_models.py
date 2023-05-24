from django.test import TestCase

from formula_tear_sheets.models import (
    FormulaImageCaption,
    FormulaTearSheet,
    FormulaTearSheetDetail,
    FormulaTearSheetFooterDetail,
)
from products.models import Category, CatSeriesItem, Item, Series


class FormulaTearSheetTest(TestCase):
    def setUp(self):
        self.storage, cat_create = Category.objects.get_or_create(name="STORAGE")
        self.lake, series_create = Series.objects.get_or_create(name="LAKE")
        self.credenza, item_create = Item.objects.get_or_create(name="CREDENZA")
        self.hutch, item_create = Item.objects.get_or_create(name="HUTCH")

        self.tear_sheet = FormulaTearSheet.objects.create(title="Bronze Credenzas")

        self.csi, csi_create = CatSeriesItem.objects.get_or_create(
            category=self.storage,
            series=self.lake,
            item=self.credenza,
            formula_tear_sheet=self.tear_sheet,
        )

        self.detail = FormulaTearSheetDetail.objects.create(
            order=1, name="detail", details="Made in NYC.", tear_sheet=self.tear_sheet
        )
        self.footer_detail = FormulaTearSheetFooterDetail.objects.create(
            order=1, name="detail", details="Made in NYC.", tear_sheet=self.tear_sheet
        )
        self.image_caption = FormulaImageCaption.objects.create(
            order_no=1,
            caption_title="LEFT",
            caption="A nice photo.",
            tear_sheet=self.tear_sheet,
        )
        self.detail_view_url = self.tear_sheet.get_absolute_url()

    def test_csi_fk_tearsheet(self):
        self.assertEqual(self.csi.formula_tear_sheet, self.tear_sheet)

    def test_tearsheet_str(self):
        self.assertEqual(f"{self.tear_sheet}", self.tear_sheet.__str__())

    def test_tearsheet_slug(self):
        self.assertEqual(self.tear_sheet.get_slug_title(), "bronze-credenzas")

    # test_list_view

    # test_printing_url

    # test_printing_url_no_list
