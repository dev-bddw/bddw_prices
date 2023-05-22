from django.db import models
from django.urls import reverse
from django.utils.text import slugify


def image_upload_to(instance, filename):
    return f"tear_sheet_images/{instance.title}/{filename}"


def gbp_sdata_json_default():
    return {
        "pt": 5,
        "col_1": 202,
        "col_2": 402,
        "col_3": 74,
        "col_4": 80,
        "col_5": 72,
        "col_6": 84,
        "pt_pr": 5,
        "pt_cap": 5,
        "d_col_1": 87,
        "d_col_2": 703,
        "font_size": 9,
        "pt_detail": 5,
        "pt_footer": 5,
    }


def json_default():
    return {
        "d_col_1": 87,
        "d_col_2": 703,
        "col_1": 87,
        "col_2": 173,
        "col_3": 499,
        "col_4": 80,
        "col_5": 54,
        "pt_cap": 5,
        "pt_detail": 5,
        "pt_footer": 5,
        "pt_pr": 5,
        "pt": 5,
        "font_size": 10,
    }


class FormulaTearSheet(models.Model):
    """
    the model for tearsheets that use formulas to generate price records
    not implemented for gbp
    """

    class TearSheetTemplate(models.TextChoices):
        a = "A", "ONE COLUMN DISPLAY"
        b = "B", "TWO COLUMN DISPLAY"
        c = "C", "RULE TYPE ABOVE"

    gbp_sdata = models.JSONField(default=gbp_sdata_json_default, blank=True, null=True)
    gbp_template = models.CharField(
        choices=TearSheetTemplate.choices, default="C", max_length=1000
    )

    template = models.CharField(
        choices=TearSheetTemplate.choices, default="B", max_length=1000
    )
    sdata = models.JSONField(default=json_default, blank=True, null=True)
    title = models.CharField(
        help_text="This will appear at the top of the tearsheet.",
        blank=True,
        null=True,
        default=None,
        max_length=1000,
    )
    image = models.ImageField(
        default="default_image.jpg",
        help_text="Usually the collage jpg containing dif items.",
        blank=True,
        null=True,
        upload_to=image_upload_to,
    )

    updated_on = models.DateTimeField(auto_now=True)

    footer_space = models.IntegerField(default=200, blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            "react_views:r_formula_tear_sheets:view-tearsheet", kwargs={"id": self.pk}
        )

    def get_absolute_gbp_url(self):
        return reverse("react_views:r_form_gbp:view-tearsheet", kwargs={"id": self.pk})

    def get_edit_url(self):
        return reverse(
            "react_views:r_formula_tear_sheets:edit-tearsheet", kwargs={"id": self.pk}
        )

    def get_printing_url(self):
        return reverse(
            "react_views:r_formula_tear_sheets:detail-view-for-print",
            kwargs={"id": self.pk},
        )

    def get_printing_url_no_list(self):
        return reverse(
            "react_views:r_formula_tear_sheets:detail-view-for-print-list",
            kwargs={"id": self.pk},
        )

    def get_gbp_printing_url(self):
        return reverse(
            "react_views:r_form_gbp:detail-view-for-print", kwargs={"id": self.pk}
        )

    def get_gbp_printing_url_no_list(self):
        return reverse(
            "react_views:r_form_gbp:detail-view-for-print-list", kwargs={"id": self.pk}
        )

    def get_slug_title(self):
        return slugify(self.title)


class FormulaTearSheetDetail(models.Model):
    tear_sheet = models.ForeignKey(
        "FormulaTearSheet",
        help_text="Details must be attached to a tearsheet.",
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=1000)
    details = models.CharField(max_length=1000)
    order = models.IntegerField(
        help_text="The order number when this record appears with like records."
    )

    def __str__(self):
        return f"{self.tear_sheet} - {self.name}"

    class Meta:
        ordering = ["order"]

    def save(self, *args, **kwargs):
        self.tear_sheet.save()
        super(FormulaTearSheetDetail, self).save(*args, **kwargs)


class FormulaTearSheetFooterDetail(models.Model):
    tear_sheet = models.ForeignKey(
        "FormulaTearSheet",
        help_text="Details must be attached to a tearsheet.",
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=1000)
    details = models.CharField(max_length=1000)
    order = models.IntegerField(
        help_text="The order number when this record appears with like records."
    )

    def __str__(self):
        return f"{self.tear_sheet} - {self.name}"

    class Meta:
        ordering = ["order"]

    def save(self, *args, **kwargs):
        self.tear_sheet.save()
        super(FormulaTearSheetFooterDetail, self).save(*args, **kwargs)


class FormulaImageCaption(models.Model):
    tear_sheet = models.ForeignKey(
        "FormulaTearSheet", blank=False, null=False, on_delete=models.CASCADE
    )
    order_no = models.IntegerField(
        help_text="The order number when this record appears with like records."
    )
    caption_title = models.CharField(
        help_text="Usually the position of the image being described.",
        blank=True,
        null=True,
        default="CAPTION",
        max_length=1000,
    )
    caption = models.CharField(
        help_text="The image caption. Usually a product description.",
        blank=True,
        null=True,
        default="This is an image caption",
        max_length=1000,
    )

    def __str__(self):
        return f"IMG {self.order_no} {self.tear_sheet}"

    class Meta:
        ordering = ["order_no"]

    def return_file_name(self):
        split_up = self.file.url.split("/")
        return split_up[-1]

    def save(self, *args, **kwargs):
        self.tear_sheet.save()
        super(FormulaImageCaption, self).save(*args, **kwargs)
