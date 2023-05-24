from django.conf import settings
from django.test import TestCase

from formula_tear_sheets.models import FormulaTearSheet
from price_records.models import (
    FormulaPriceListPriceRecord,
    FormulaPriceRecord,
    PriceListPriceRecord,
    PriceRecord,
)
from products.models import Category, CatSeriesItem, Item, Series
from tear_sheets.models import TearSheet


class PriceRecordTests(TestCase):
    def setUp(self):
        """
        setup one CSI w/ tearsheet, one CSI without
        setup one PriceRecord w/ list_price, another without

        """

        self.storage, cat_create = Category.objects.get_or_create(name="STORAGE")
        self.lake, series_create = Series.objects.get_or_create(name="LAKE")
        self.credenza, item_create = Item.objects.get_or_create(name="CREDENZA")
        self.hutch, item_create = Item.objects.get_or_create(name="HUTCH")

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

        self.record, record_create = PriceRecord.objects.update_or_create(
            bin_id=200,
            defaults={
                "cat_series_item": self.CSI,
                "rule_type": "SIZES",
                "rule_display_1": "10 x 10 x 10",
                "rule_display_2": "Drawers",
                "list_price": "1000",
            },
        )

        self.no_price_record, np_record_create = PriceRecord.objects.update_or_create(
            bin_id=102,
            defaults={
                "cat_series_item": self.CSI_no_tearsheet,
                "rule_type": "SIZES",
                "rule_display_1": "10 x 10 x 10",
                "rule_display_2": "Drawers",
            },
        )

    def test_price_error(self):
        self.assertEqual(
            self.no_price_record.get_net_price(), "LIST PRICE MUST HAVE INT VALUE."
        )

    def test_get_net_price(self):
        lp = int(self.record.list_price)
        multiplier = settings.NET_PRICE_MULTIPLIER

        self.assertEqual(self.record.get_net_price(), str(int(lp * multiplier)))

    def test_save_net_price(self):
        self.record.save()
        self.assertEqual("850", self.record.net_price)

    def test_string(self):
        self.assertEqual(
            self.record.__str__(), f"{self.record.cat_series_item} PRICE RECORD"
        )


class PriceListRecordTests(TestCase):
    def setUp(self):
        self.storage, cat_create = Category.objects.get_or_create(name="STORAGE")
        self.lake, series_create = Series.objects.get_or_create(name="LAKE")
        self.credenza, item_create = Item.objects.get_or_create(name="CREDENZA")
        self.hutch, item_create = Item.objects.get_or_create(name="HUTCH")

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
            self.no_price_record,
            np_record_create,
        ) = PriceListPriceRecord.objects.update_or_create(
            bin_id=102,
            defaults={
                "cat_series_item": self.CSI_no_tearsheet,
                "rule_type": "SIZES",
                "rule_display_1": "10 x 10 x 10",
                "rule_display_2": "Drawers",
            },
        )

    def test_price_error(self):
        self.assertEqual(
            self.no_price_record.get_net_price(),
            "Please make sure your LIST PRICE has an integer value.",
        )

    def test_get_net_price(self):
        self.assertEqual("850", self.record.get_net_price())

    def test_save_net_price(self):
        self.record.save()
        self.assertEqual("850", self.record.net_price)

    def test_string(self):
        self.assertEqual(
            self.record.__str__(), f"{self.record.cat_series_item} PRICE RECORD"
        )


class FormulaPriceRecordTests(TestCase):
    def setUp(self):
        self.storage, cat_create = Category.objects.get_or_create(name="STORAGE")
        self.lake, series_create = Series.objects.get_or_create(name="LAKE")
        self.credenza, item_create = Item.objects.get_or_create(name="CREDENZA")
        self.hutch, item_create = Item.objects.get_or_create(name="HUTCH")

        self.CSI, csi_create = CatSeriesItem.objects.get_or_create(
            formula="[length] * [depth]",
            category=self.storage,
            series=self.lake,
            item=self.credenza,
            formula_tear_sheet=FormulaTearSheet.objects.create(),
        )

        self.CSI_no_tearsheet, csi_create = CatSeriesItem.objects.get_or_create(
            category=self.storage,
            series=self.lake,
            item=self.hutch,
        )

        self.record, record_create = FormulaPriceRecord.objects.update_or_create(
            defaults={
                "cat_series_item": self.CSI,
                "length": 20,
                "depth": 50,
                "rule_type": "SIZES",
                "rule_display_1": "[length] L X [depth] X D",
            }
        )

        (
            self.no_formula_record,
            np_record_create,
        ) = FormulaPriceRecord.objects.update_or_create(
            defaults={
                "cat_series_item": self.CSI_no_tearsheet,
                "rule_type": "SIZES",
                "length": 20,
                "depth": 50,
                "list_price": "Alpha",
                "rule_display_1": "10 x 10 x 10",
                "rule_display_2": "Drawers",
            },
        )

    def test_price_no_formula(self):
        self.no_formula_record.save()

        self.assertEqual(self.no_formula_record.list_price, 0)

    def test_net_price(self):
        self.record.save()
        self.no_formula_record.save()

        self.assertEqual(
            self.record.net_price, str(int(settings.NET_PRICE_MULTIPLIER * 1000))
        )
        self.assertEqual(self.no_formula_record.get_net_price(), "0")

    def test_price_formula(self):
        self.record.save()

        self.assertEqual(self.record.list_price, 1000)

    def test_formula_translation(self):
        translation = self.record.return_rule_display_1()

        self.assertEqual(translation, "20 L X 50 X D")

    def test_value_dict(self):
        value_dict = self.record.return_value_dict()

        self.assertEqual(type({}), type(value_dict))
        self.assertEqual(20, value_dict["length"])
        self.assertEqual(50, value_dict["depth"])


class FormulaPriceListPriceRecordTests(TestCase):
    def setUp(self):
        self.storage, cat_create = Category.objects.get_or_create(name="STORAGE")
        self.lake, series_create = Series.objects.get_or_create(name="LAKE")
        self.credenza, item_create = Item.objects.get_or_create(name="CREDENZA")
        self.hutch, item_create = Item.objects.get_or_create(name="HUTCH")

        self.CSI, csi_create = CatSeriesItem.objects.get_or_create(
            formula="[length] * [depth]",
            category=self.storage,
            series=self.lake,
            item=self.credenza,
            tear_sheet=TearSheet.objects.create(),
        )

        self.CSI_no_formula, csi_create = CatSeriesItem.objects.get_or_create(
            category=self.storage,
            series=self.lake,
            item=self.hutch,
        )

        (
            self.record,
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

        (
            self.no_formula_record,
            np_record_create,
        ) = FormulaPriceListPriceRecord.objects.update_or_create(
            defaults={
                "cat_series_item": self.CSI_no_formula,
                "length": 20,
                "depth": 50,
                "rule_type": "SIZES",
                "rule_display_1": "10 x 10 x 10",
                "rule_display_2": "Drawers",
                "list_price": "Alpha",
            },
        )

    def test_price_formula(self):
        self.record.save()

        self.assertEqual(self.record.list_price, 1000)

    def test_price_no_formula(self):
        self.no_formula_record.save()

        self.assertEqual(self.no_formula_record.list_price, 0)

    def test_net_price(self):
        self.record.save()
        self.no_formula_record.save()

        self.assertEqual(
            self.record.net_price, str(int(settings.NET_PRICE_MULTIPLIER * 1000))
        )
        self.assertEqual(self.no_formula_record.get_net_price(), "0")

    def test_formula_translation(self):
        translation = self.record.return_rule_display_1()

        self.assertEqual(translation, "20 L X 50 X D")

    def test_value_dict(self):
        value_dict = self.record.return_value_dict()

        self.assertEqual(type({}), type(value_dict))
        self.assertEqual(20, value_dict["length"])
        self.assertEqual(50, value_dict["depth"])
