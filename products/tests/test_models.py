from django.test import TestCase

from products.models import Category, CatSeriesItem, Item, Series
from tear_sheets.models import TearSheet


class TestCategorySeriesItems(TestCase):
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

    def test_simple_save(self):

        self.CSI.save()

    def test_duplicate(self):

        with self.assertRaisesMessage(
            ValueError, "This Category Series Item already exists"
        ):

            self.CSI, csi_create = CatSeriesItem.objects.get_or_create(
                category=self.storage,
                series=self.lake,
                item=self.credenza,
                tear_sheet=TearSheet.objects.create(),
            )
