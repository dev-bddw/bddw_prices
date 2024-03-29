from django.db import models


class Category(models.Model):
    name = models.CharField(unique=True, blank=True, null=True, max_length=200)
    order = models.IntegerField(blank=True, null=True)
    pricelist_ignore = models.BooleanField(
        default=False,
        help_text="If selected (true) rules for this category will not show up in pricelist",
    )

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["order"]

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        for obj in CatSeriesItem.objects.filter(category=self):
            if (obj.cat_order is not None) and (obj.cat_order != ""):
                self.order = obj.cat_order
                break

        super(Category, self).save(*args, **kwargs)


class Series(models.Model):
    name = models.CharField(unique=True, blank=True, null=True, max_length=200)

    class Meta:
        verbose_name_plural = "Series"

    def __str__(self):
        return f"{self.name}"


class Item(models.Model):
    name = models.CharField(unique=True, blank=True, null=True, max_length=200)

    class Meta:
        verbose_name_plural = "Items"

    def __str__(self):
        return f"{self.name}"


class CatSeriesItem(models.Model):
    category = models.ForeignKey(
        "products.Category", blank=False, null=False, on_delete=models.DO_NOTHING
    )
    series = models.ForeignKey(
        "products.Series", blank=False, null=False, on_delete=models.DO_NOTHING
    )
    item = models.ForeignKey(
        "products.Item", blank=False, null=False, on_delete=models.DO_NOTHING
    )

    cat_order = models.IntegerField(blank=True, null=True)
    series_order = models.IntegerField(blank=True, null=True)
    item_order = models.IntegerField(blank=True, null=True)

    opt_series_item_display = models.CharField(
        blank=True,
        null=True,
        default=None,
        help_text="Display alternate series item string?",
        max_length=200,
    )

    formula = models.CharField(
        blank=True,
        null=True,
        default=None,
        help_text="The string version of the formula",
        max_length=200,
    )
    tear_sheet = models.ForeignKey(
        "tear_sheets.TearSheet", blank=True, null=True, on_delete=models.SET_NULL
    )

    formula_tear_sheet = models.ForeignKey(
        "formula_tear_sheets.FormulaTearSheet",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    def return_series_item(self):
        return (
            f"{self.series} {self.item}"
            if self.opt_series_item_display is None
            else self.opt_series_item_display
        )

    def save(self, *args, **kwargs):
        # roundabout way of ensuring unique for cat-series-item fk's
        try:
            item = CatSeriesItem.objects.get(
                category=self.category, series=self.series, item=self.item
            )
            if item.pk == self.pk:
                super(CatSeriesItem, self).save(*args, **kwargs)
            else:
                raise ValueError("This Category Series Item already exists")

        except CatSeriesItem.DoesNotExist:
            super(CatSeriesItem, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.category} - {self.series} - {self.item}"

    def return_translation(self):
        try:
            f = self.formula.replace("[", "").replace("]", "")

            import re

            formula = re.sub(r"([a-z])\s([a-z])", "\\1_\\2", f)

            return formula

        except AttributeError:
            pass

    def return_price_records(self):
        if self.formula is None or "":
            from price_records.models import PriceRecord

            return PriceRecord.objects.filter(cat_series_item_id=self.pk)
        else:
            from price_records.models import FormulaPriceRecord

            return FormulaPriceRecord.objects.filter(cat_series_item_id=self.pk)

    def has_formula(self):
        return True if self.formula not in ["", None] else False

    class Meta:
        verbose_name = "Category Series Item"
        verbose_name_plural = "Category Series Items"
        ordering = ["cat_order", "series_order", "item_order"]
