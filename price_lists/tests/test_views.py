from django.test import TestCase
from django.urls import reverse

from price_records.models import FormulaPriceListPriceRecord, PriceListPriceRecord
from products.models import Category, CatSeriesItem, Item, Series
from tear_sheets.models import TearSheet


class TestListView(TestCase):
    def setUp(self):
        self.storage, cat_create = Category.objects.get_or_create(name="STORAGE")
        self.lake, series_create = Series.objects.get_or_create(name="LAKE")
        self.credenza, item_create = Item.objects.get_or_create(name="CREDENZA")
        self.hutch, item_create = Item.objects.get_or_create(name="HUTCH")
        self.cabinet, item_create = Item.objects.get_or_create(name="CABINET")

        self.CSI, csi_create = CatSeriesItem.objects.get_or_create(
            category=self.storage,
            series=self.lake,
            item=self.credenza,
            tear_sheet=TearSheet.objects.create(),
        )

        self.CSI_no_tearsheet, csi_create = CatSeriesItem.objects.get_or_create(
            category=self.storage,
            series=self.lake,
            item=self.hutch,
        )

        self.empty_csi, csi_create = CatSeriesItem.objects.get_or_create(
            category=self.storage,
            series=self.lake,
            item=self.cabinet,
        )

        self.record, record_create = PriceListPriceRecord.objects.update_or_create(
            bin_id=200,
            defaults={
                "cat_series_item": self.CSI,
                "rule_type": "SIZES",
                "rule_display_1": "10 x 10 x 10",
                "rule_display_2": "Drawers",
                "list_price": "1000",
            },
        )

        (
            self.formula_record,
            record_create,
        ) = FormulaPriceListPriceRecord.objects.update_or_create(
            defaults={
                "cat_series_item": self.CSI,
                "length": 20,
                "depth": 50,
                "rule_type": "SIZES",
                "rule_display_1": "[length] L X [depth] X D",
            }
        )

        self.list_url = reverse("pricelists:list")

    def test_list_view(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.record.rule_display_1)
        self.assertContains(response, self.formula_record.rule_display_1)
