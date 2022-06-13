# Create your models here.
from django.conf import settings
from django.db import models


# Create your models here.
class PriceRecord(models.Model):
    class RecordType(models.TextChoices):
        size = "SIZES", "SIZES"
        finish = "FINISH", "FINISH"
        any = "ANY", "ANY"

    cat_series_item = models.ForeignKey(
        "products.CatSeriesItem", blank=False, null=False, on_delete=models.CASCADE
    )

    rule_type = models.CharField(
        help_text="What kind of price record is this?",
        choices=RecordType.choices,
        default=RecordType.size,
        max_length=200,
    )

    rule_display_1 = models.CharField(help_text="ex. 67 x 19 x 29 H", max_length=200)
    rule_display_2 = models.CharField(
        help_text="ex. / 2 STANDARD DRAWERS / 2 CABS ",
        blank=True,
        null=True,
        max_length=200,
    )

    list_price = models.CharField(max_length=200)
    net_price = models.CharField(max_length=200)

    order = models.IntegerField(
        help_text="The order number when this Price Record appears with others."
    )

    bin_id = models.IntegerField(
        blank=True, null=True, help_text="This is the bin id number for the price rule"
    )

    class Meta:
        ordering = ["order"]

    def get_net_price(self):
        try:
            return (
                (str(round(int(self.list_price) * settings.NET_PRICE_MULTIPLIER)))
                if self.list_price is not None
                else 0
            )
        except ValueError:
            return "Please make sure your LIST PRICE has an integer value."

    def __str__(self):
        return f"{self.cat_series_item} PRICE RECORD"

    def save(self, *args, **kwargs):
        self.net_price = self.get_net_price()
        super(PriceRecord, self).save(*args, **kwargs)


class FormulaPriceRecord(models.Model):
    cat_series_item = models.ForeignKey(
        "products.CatSeriesItem", on_delete=models.DO_NOTHING
    )

    rule_type = models.CharField(
        help_text="What kind of price record is this?",
        max_length=200,
        blank=True,
        null=True,
    )

    depth = models.IntegerField(null=True, blank=True)
    length = models.IntegerField(null=True, blank=True)
    width = models.IntegerField(null=True, blank=True)
    diameter = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    footboard_height = models.IntegerField(null=True, blank=True)
    headboard_height = models.IntegerField(null=True, blank=True)
    headboard_width = models.IntegerField(null=True, blank=True)
    seat_fabric_yardage = models.IntegerField(null=True, blank=True)
    seat_back_height = models.IntegerField(null=True, blank=True)
    seat_height = models.IntegerField(null=True, blank=True)
    inset = models.IntegerField(null=True, blank=True)

    rule_display_1 = models.CharField(help_text="ex. 67 x 19 x 29 H", max_length=200)
    rule_display_2 = models.CharField(
        help_text="ex. / 2 STANDARD DRAWERS / 2 CABS",
        blank=True,
        null=True,
        max_length=200,
    )

    list_price = models.CharField(null=True, blank=True, max_length=200)
    net_price = models.CharField(null=True, blank=True, max_length=200)

    def save(self, *args, **kwargs):
        self.list_price = self.get_price()
        self.net_price = self.get_net_price()

        super(FormulaPriceRecord, self).save(*args, **kwargs)

    def return_value_dict(self):

        return {
            "depth": self.depth,
            "length": self.length,
            "width": self.width,
            "diameter": self.diameter,
            "height": self.height,
            "footboard_height": self.footboard_height,
            "headboard_height": self.headboard_height,
            "headboard_width": self.headboard_width,
            "seat_fabric_yardage": self.seat_fabric_yardage,
            "seat_back_height": self.seat_back_height,
            "seat_height": self.seat_height,
            "inset": self.inset,
        }

    def get_net_price(self):
        try:
            return (
                (str(round(int(self.list_price) * settings.NET_PRICE_MULTIPLIER)))
                if self.list_price is not None
                else 0
            )
        except ValueError:
            return "Please make sure your LIST PRICE has an integer value."

    def get_price(self):
        try:
            return round(
                eval(
                    self.cat_series_item.return_translation(), self.return_value_dict()
                )
            )
        except NameError:
            return "Price Record values didn't match forumula. Double check for correct variable defs in price record."
        except ValueError:
            return "The Category Series Item doesn't have a formula defined."
        except TypeError:
            return "Price Record values didn't match forumula. Double check for correct variable defs in price record."

    def __str__(self):
        return f"{self.cat_series_item}: {self.cat_series_item.return_translation()}"
