from django.db import models


class Category(models.Model):
    name = models.CharField(unique=True, blank=True, null=True, max_length=200)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return f"{self.name}"


class Series(models.Model):
    name = models.CharField(unique=True, blank=True, null=True, max_length=200)

    class Meta:
        verbose_name_plural = "Series"

    def __str__(self):
        return f"{self.name}"


class Item(models.Model):
    name = models.CharField(unique=True, blank=True, null=True, max_length=200)

    class Meta:
        pass

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

    def __str__(self):
        return f"{self.category} - {self.series} - {self.item}"

    def return_translation(self):
        if self.formula is not None or "":
            f = self.formula.replace("[", "").replace("]", "")
            import re

            formula = re.sub("([a-z])\s([a-z])", "\\1_\\2", f)
            return formula
        else:
            "raise ValueError"

    def return_price_records(self):
        if self.formula is None or "":
            from price_records.models import PriceRecord

            return PriceRecord.objects.filter(cat_series_item_id=self.pk)
        else:
            from price_records.models import FormulaPriceRecord

            return FormulaPriceRecord.objects.filter(cat_series_item_id=self.pk)

    class Meta:
        verbose_name = "Category Series Item"
        verbose_name_plural = "Category Series Items"
