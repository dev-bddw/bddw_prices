# Create your models here.
from django.conf import settings
from django.db import models
from django.utils import timezone


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
        default="",
        max_length=200,
    )

    list_price = models.CharField(max_length=200)
    net_price = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="This value will be calculated on record save.",
    )

    order = models.IntegerField(
        help_text="The order number when this Price Record appears with others."
    )

    bin_id = models.IntegerField(
        blank=True, null=True, help_text="This is the bin id number for the price rule"
    )

    class Meta:
        ordering = ["order", "rule_display_1"]

    def get_net_price(self):
        try:
            return (
                str(int(int(self.list_price) * settings.NET_PRICE_MULTIPLIER))
                if self.list_price is not None
                else 0
            )
        except ValueError:
            return "LIST PRICE MUST HAVE INT VALUE."

    def __str__(self):
        return f"{self.cat_series_item} PRICE RECORD"

    def save(self, *args, **kwargs):
        self.net_price = self.get_net_price()

        try:
            order = int(self.list_price)
        except ValueError:
            order = 0

        self.order = order

        if self.cat_series_item.tear_sheet is None:
            pass
        else:
            self.cat_series_item.tear_sheet.save()

        super(PriceRecord, self).save(*args, **kwargs)


class PriceListPriceRecord(models.Model):
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
        default="",
        max_length=200,
    )

    list_price = models.CharField(max_length=200)
    net_price = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="This value will be calculated on record save.",
    )

    order = models.IntegerField(
        help_text="The order number when this Price Record appears with others."
    )

    bin_id = models.IntegerField(
        blank=True, null=True, help_text="This is the bin id number for the price rule"
    )

    updated_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        ordering = ["order"]

    def get_net_price(self):
        try:
            return (
                str(int(int(self.list_price) * settings.NET_PRICE_MULTIPLIER))
                if self.list_price is not None
                else 0
            )
        except ValueError:
            return "Please make sure your LIST PRICE has an integer value."

    def __str__(self):
        return f"{self.cat_series_item} PRICE RECORD"

    def save(self, *args, **kwargs):
        self.net_price = self.get_net_price()

        try:
            order = int(self.list_price)
        except ValueError:
            order = 0

        self.order = order

        if self.cat_series_item.tear_sheet is None:
            pass
        else:
            self.cat_series_item.tear_sheet.save()

        super(PriceListPriceRecord, self).save(*args, **kwargs)


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

    rule_display_1 = models.CharField(
        blank=True, null=True, help_text="ex. 67 x 19 x 29 H", max_length=200
    )
    rule_display_2 = models.CharField(
        help_text="ex. / 2 STANDARD DRAWERS / 2 CABS",
        default="",
        blank=True,
        null=True,
        max_length=200,
    )

    list_price = models.CharField(null=True, blank=True, max_length=200)
    net_price = models.CharField(null=True, blank=True, max_length=200)

    def save(self, *args, **kwargs):
        self.list_price = self.get_price()
        self.net_price = self.get_net_price()
        self.rule_display_1 = self.return_display_rule()

        if self.cat_series_item.formula_tear_sheet is None:
            pass
        else:
            self.cat_series_item.formula_tear_sheet.save()

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
                str(int(int(self.list_price) * settings.NET_PRICE_MULTIPLIER))
                if self.list_price is not None
                else 0
            )
        except ValueError:
            return "Please make sure your LIST PRICE has an integer value."

    def return_display_rule(self):
        st = ""
        for key, value in self.return_value_dict().items():
            if value not in [0, None, ""]:
                st += f"{value} {key.upper()[0]} X "
        st = st[:-2]
        return st

    def evaluate(self):
        return (
            eval(self.cat_series_item.return_translation(), self.return_value_dict())
            if self.cat_series_item != ""
            else 0
        )

    def get_price(self):
        if self.cat_series_item.has_formula():
            try:
                return 100 * round(int(self.evaluate()) * 0.01)
            except NameError:
                return "Price Record values != forumula. Double check for correct variable defs in price record."
            except ValueError:
                return "The Category Series Item doesn't have a formula defined."
            except TypeError:
                return "Price Record values != forumula. Double check for correct variable defs in price record."

        else:
            return 0

    def __str__(self):
        return f"{self.cat_series_item}: {self.cat_series_item.return_translation()}"


class FormulaPriceListPriceRecord(models.Model):
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

    rule_display_1 = models.CharField(
        blank=True,
        default=" ",
        null=True,
        help_text="ex. 67 x 19 x 29 H",
        max_length=200,
    )
    rule_display_2 = models.CharField(
        help_text="ex. / 2 STANDARD DRAWERS / 2 CABS",
        default=" ",
        blank=True,
        null=True,
        max_length=200,
    )

    updated_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    list_price = models.CharField(null=True, blank=True, max_length=200)
    net_price = models.CharField(null=True, blank=True, max_length=200)

    def save(self, *args, **kwargs):
        self.list_price = self.get_price()
        self.net_price = self.get_net_price()
        # self.rule_display_1 = self.return_display_rule()

        if self.cat_series_item.formula_tear_sheet is None:
            pass

        else:
            self.cat_series_item.formula_tear_sheet.save()

        self.updated_on = timezone.now()

        super(FormulaPriceListPriceRecord, self).save(*args, **kwargs)

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
                str(int(int(self.list_price) * settings.NET_PRICE_MULTIPLIER))
                if self.list_price is not None
                else 0
            )
        except ValueError:
            return "Please make sure your LIST PRICE has an integer value."

    def return_rule_display_1_translation(self):

        f = self.rule_display_1.replace("[", "{").replace("]", "}")

        import re

        rule_display_1 = re.sub("([a-z])\s([a-z])", "\\1_\\2", f)

        return rule_display_1

    def return_rule_display_1(self):
        if "[" in self.rule_display_1:

            template = self.return_rule_display_1_translation()
            variables = self.return_value_dict()
            return template.format(**variables)

        else:
            return self.rule_display_1

    def evaluate(self):
        return (
            eval(self.cat_series_item.return_translation(), self.return_value_dict())
            if self.cat_series_item != ""
            else 0
        )

    def get_price(self):
        if self.cat_series_item.has_formula():
            try:
                return 100 * round(int(self.evaluate()) * 0.01)
            except NameError:
                return "Price Record values != forumula. Double check for correct variable defs in price record."
            except ValueError:
                return "The Category Series Item doesn't have a formula defined."
            except TypeError:
                return "Price Record values != forumula. Double check for correct variable defs in price record."

        else:
            return 0

    def __str__(self):
        return f"{self.cat_series_item}: {self.cat_series_item.return_translation()}".upper()

    class Meta:
        ordering = ["list_price"]
