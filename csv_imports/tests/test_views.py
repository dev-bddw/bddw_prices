from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from price_records.models import (
    FormulaPriceListPriceRecord,
    FormulaPriceRecord,
    PriceListPriceRecord,
    PriceRecord,
)
from products.models import Category, CatSeriesItem, Item, Series


class TestUploadViews(TestCase):

    """
    test csv upload views
    """

    def setUp(self):

        User = get_user_model()

        self.user = User.objects.create(username="bilbo", password="baggins")
        self.client = Client()
        self.client.force_login(self.user)

        self.pricing_csv_upload_url = reverse("csv_imports:upload")
        self.formula_csv_upload_url = reverse("csv_imports:upload_formula")
        self.sorting_csv_upload_url = reverse("csv_imports:sorting_upload")

    def test_pricing_upload(self):

        with open(
            settings.ROOT_DIR / "csv_imports/tests/test_csv/pricing_upload.csv"
        ) as csv_file:

            response = self.client.post(self.pricing_csv_upload_url, {"file": csv_file})

        created_records, created_pricelist_records = (
            PriceRecord.objects.all(),
            PriceListPriceRecord.objects.all(),
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(457, len(created_records))
        self.assertEqual(974, len(created_pricelist_records))

    def test_formula_record_upload(self):
        with open(
            settings.ROOT_DIR / "csv_imports/tests/test_csv/formula_upload.csv"
        ) as csv_file:

            response = self.client.post(self.formula_csv_upload_url, {"file": csv_file})

        created_records, created_pricelist_records = (
            FormulaPriceRecord.objects.all(),
            FormulaPriceListPriceRecord.objects.all(),
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(23, len(created_records))
        self.assertEqual(66, len(created_pricelist_records))

    def test_sorting_record_upload(self):
        with open(
            settings.ROOT_DIR / "csv_imports/tests/test_csv/sorting_upload.csv"
        ) as csv_file:

            response = self.client.post(self.sorting_csv_upload_url, {"file": csv_file})

        self.assertEqual(response.status_code, 200)


class TestExportViews(TestCase):
    """
    tests views that return csv w/ db info
    """

    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create(username="bilbo", password="baggins")
        self.client = Client()
        self.client.force_login(self.user)

        csi, created = CatSeriesItem.objects.update_or_create(
            defaults={
                "category": Category.objects.create(name="STORAGE"),
                "series": Series.objects.create(name="LEATHER"),
                "item": Item.objects.create(name="CREDENZA"),
                "formula": "[length] * [height]",
                "cat_order": 1,
                "series_order": 1,
                "item_order": 1,
            }
        )

        PriceListPriceRecord.objects.create(
            rule_type="SIZES", cat_series_item=csi, list_price="1000", order=1
        )
        PriceRecord.objects.create(
            rule_type="SIZES", cat_series_item=csi, list_price="1000", order=1
        )
        FormulaPriceListPriceRecord.objects.create(
            length=10, height=10, cat_series_item=csi
        )
        FormulaPriceRecord.objects.create(length=10, height=10, cat_series_item=csi)

        self.export_sorting_records_url = reverse("csv_imports:sorting_export")
        self.export_formula_records_url = reverse("csv_imports:export_formula")
        self.export_pricelist_records_url = reverse("csv_imports:export_price_records")
        self.export_price_records_url = reverse("csv_imports:export_pricelist_records")

    def test_export_sorting(self):

        response = self.client.get(self.export_sorting_records_url)

        self.assertEqual(response.status_code, 200)

    def test_export_formula(self):

        response = self.client.get(self.export_formula_records_url)

        self.assertEqual(response.status_code, 200)

    def test_export_pricelist(self):

        response = self.client.get(self.export_pricelist_records_url)

        self.assertEqual(response.status_code, 200)

    def test_export_price(self):

        response = self.client.get(self.export_price_records_url)

        self.assertEqual(response.status_code, 200)


class TestTemplateViews(TestCase):
    """
    tests views that create templates aka csv files w/ one row
    """

    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create(username="bilbo", password="baggins")
        self.client = Client()
        self.client.force_login(self.user)

        self.formula_template_url = reverse("csv_imports:form_template")
        self.normal_template_url = reverse("csv_imports:normal_template")
        self.sorting_template_url = reverse("csv_imports:sorting_upload")

    def test_normal_template(self):

        response = self.client.get(self.normal_template_url)

        self.assertEqual(response.status_code, 200)

    def test_formula_template(self):

        response = self.client.get(self.formula_template_url)

        self.assertEqual(response.status_code, 200)

    def test_sorting_template(self):

        response = self.client.get(self.sorting_template_url)

        self.assertEqual(response.status_code, 200)