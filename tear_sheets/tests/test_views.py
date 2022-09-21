from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from price_records.models import PriceRecord
from products.models import Category, CatSeriesItem, Item, Series
from tear_sheets.models import (
    ImageCaption,
    TearSheet,
    TearSheetDetail,
    TearSheetFooterDetail,
)


class TearSheetTest(TestCase):
    def setUp(self):

        User = get_user_model()

        self.user = User.objects.create(username="bilbo", password="baggins")

        self.storage, cat_create = Category.objects.get_or_create(name="STORAGE")
        self.lake, series_create = Series.objects.get_or_create(name="LAKE")
        self.credenza, item_create = Item.objects.get_or_create(name="CREDENZA")
        self.hutch, item_create = Item.objects.get_or_create(name="HUTCH")

        self.tear_sheet = TearSheet.objects.create(title="Bronze Credenzas")

        self.csi, csi_create = CatSeriesItem.objects.get_or_create(
            category=self.storage,
            series=self.lake,
            item=self.credenza,
            tear_sheet=self.tear_sheet,
        )

        self.detail = TearSheetDetail.objects.create(
            order=1, name="detail", details="Made in NYC.", tear_sheet=self.tear_sheet
        )
        self.footer_detail = TearSheetFooterDetail.objects.create(
            order=1, name="detail", details="Made in NYC.", tear_sheet=self.tear_sheet
        )
        self.image_caption = ImageCaption.objects.create(
            order_no=1,
            caption_title="LEFT",
            caption="A nice photo.",
            tear_sheet=self.tear_sheet,
        )

        self.price_record = PriceRecord.objects.create(
            cat_series_item=self.csi,
            rule_type="SIZES",
            rule_display_1="1 X 2 X 3",
            rule_display_2="Romney Finish",
        )

        self.detail_view_url = self.tear_sheet.get_absolute_url()
        self.edit_view_url = self.tear_sheet.get_edit_url()
        self.print_view_url = self.tear_sheet.get_printing_url()
        self.print_url_no_list = self.tear_sheet.get_printing_url_no_list()

    def test_detail_view(self):

        client = Client()

        client.force_login(self.user)

        response = client.get(self.detail_view_url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.tear_sheet.title)
        self.assertContains(response, self.price_record.rule_display_1)

    def test_edit_view(self):

        client = Client()

        client.force_login(self.user)

        response = client.get(self.edit_view_url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.tear_sheet.title)

    def test_printing_view(self):

        client = Client()

        client.force_login(self.user)

        response = self.client.get(self.print_view_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.tear_sheet.title)

    def test_printing_view_no_list(self):

        client = Client()

        client.force_login(self.user)

        response = self.client.get(self.print_url_no_list)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.tear_sheet.title)

    def test_change_template_hx(self):

        client = Client()

        client.force_login(self.user)

        url = reverse("tearsheets:change_template", kwargs={"pk": self.tear_sheet.pk})

        response = client.post(url, {"template": "C"})

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "RULE DISPLAY ABOVE")

    def test_change_title_hx(self):

        client = Client()

        client.force_login(self.user)

        url = reverse("tearsheets:change_title", kwargs={"pk": self.tear_sheet.pk})

        response = client.post(url, {"title": "NEW TITLE"})

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "NEW TITLE")

    # def test_change_image_hx(self):
    #     pass

    def test_change_caption_hx(self):

        client = Client()

        client.force_login(self.user)

        url = reverse("tearsheets:change_caption", kwargs={"pk": self.image_caption.pk})

        response = client.post(
            url, {"title": "Top Right", "caption": "Two men by the river."}
        )

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "Two men by the river.")

    def test_change_detail_hx(self):

        client = Client()

        client.force_login(self.user)

        url = reverse("tearsheets:change_detail", kwargs={"pk": self.detail.pk})

        response = client.post(
            url, {"name": "Lamp", "details": "Two colors to choose from."}
        )

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "Two colors to choose from.")

    def test_change_price_record_hx(self):

        client = Client()

        client.force_login(self.user)

        url = reverse(
            "tearsheets:change_price_record", kwargs={"pk": self.price_record.pk}
        )

        response = client.post(
            url,
            {
                "rule_type": "Lamp",
                "rule_display_1": "Neptune",
                "rule_display_2": "Manhattan",
                "list_price": "10000",
            },
        )

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "Neptune")
        self.assertContains(response, "Manhattan")

    def test_change_footer_detail_hx(self):

        client = Client()

        client.force_login(self.user)

        url = reverse(
            "tearsheets:change_footer_detail", kwargs={"pk": self.footer_detail.pk}
        )

        response = client.post(
            url, {"name": "Disclaimer", "details": "BDDW loves its customers!"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Disclaimer")
        self.assertContains(response, "BDDW loves its customers!")

    def test_create_caption_hx(self):

        client = Client()

        client.force_login(self.user)

        url = reverse("tearsheets:create_caption", kwargs={"pk": self.tear_sheet.pk})

        response = client.post(
            url, {"title": "Top Right", "caption": "Two men by the river."}
        )

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "Two men by the river.")

    def test_create_detail_hx(self):
        client = Client()

        client.force_login(self.user)

        url = reverse("tearsheets:create_detail", kwargs={"pk": self.tear_sheet.pk})

        response = client.post(
            url, {"name": "Lamp", "details": "Two colors to choose from."}
        )

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "Two colors to choose from.")

    def test_create_price_record_hx(self):
        client = Client()

        client.force_login(self.user)

        url = reverse("tearsheets:create_price_record")

        response = client.post(
            url,
            {
                "rule_type": "Lamp",
                "rule_display_1": "Neptune",
                "rule_display_2": "Manhattan",
                "list_price": "10000",
                "cat_series_item": self.csi.pk,
            },
        )

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "Neptune")
        self.assertContains(response, "Manhattan")

    def test_create_footer_detail_hx(self):
        client = Client()

        client.force_login(self.user)

        url = reverse(
            "tearsheets:create_footer_detail", kwargs={"pk": self.tear_sheet.pk}
        )

        response = client.post(
            url, {"name": "Disclaimer", "details": "BDDW loves its customers!"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Disclaimer")
        self.assertContains(response, "BDDW loves its customers!")
