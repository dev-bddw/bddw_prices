from django.db import models
from django.urls import reverse
from django.utils.text import slugify


def image_upload_to(instance, filename):
    return f"tear-sheet-images/{filename}"


class Detail(models.Model):
    tear_sheet = models.ForeignKey(
        "TearSheet",
        help_text="Details must be attached to a tearsheet.",
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )
    name = models.CharField(default="", blank=True, null=True, max_length=1000)
    details = models.CharField(max_length=1000)
    order = models.IntegerField(
        help_text="The order number when this record appears with like records."
    )

    def __str__(self):
        return f"{self.tear_sheet} - {self.name}"

    class Meta:
        ordering = ["order"]
        abstract = True

    def save(self, *args, **kwargs):
        self.tear_sheet.save()
        super(Detail, self).save(*args, **kwargs)


class TearSheetDetail(Detail):
    pass


class TearSheetFooterDetail(Detail):
    pass


class TearSheet(models.Model):
    def json_default():
        return {
            "col_1": 10,
            "col_2": 35,
            "col_3": 35,
            "col_4": 10,
            "col_5": 10,
            "d_col_1": 10,
            "d_col_2": 90,
            "pt_cap": 5,
            "pt_detail": 5,
            "pt_footer": 5,
            "pt_pr": 5,
            "font_size": 10,
        }

    def sdata_json_default(self):
        return self.json_default()

    def gbp_sdata_json_default():
        return {
            "col_1": 10,
            "col_2": 35,
            "col_3": 35,
            "col_4": 5,
            "col_5": 5,
            "col_6": 5,
            "col_7": 5,
            "d_col_1": 10,
            "d_col_2": 90,
            "pt_cap": 5,
            "pt_detail": 5,
            "pt_footer": 5,
            "pt_pr": 5,
            "font_size": 10,
        }

    class TearSheetTemplate(models.TextChoices):
        a = "A", "ONE COLUMN DISPLAY"
        b = "B", "TWO COLUMN DISPLAY"
        c = "C", "RULE TYPE ABOVE"

    sdata = models.JSONField(default=sdata_json_default, blank=True, null=True)
    gbp_sdata = models.JSONField(default=gbp_sdata_json_default, blank=True, null=True)
    gbp_template = models.CharField(
        choices=TearSheetTemplate.choices, default="C", max_length=1000
    )
    template = models.CharField(
        choices=TearSheetTemplate.choices, default="B", max_length=1000
    )

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
            "react_views:r_tear_sheets:view-tearsheet", kwargs={"id": self.pk}
        )

    def get_edit_url(self):
        return reverse(
            "react_views:r_tear_sheets:edit-tearsheet", kwargs={"id": self.pk}
        )

    def get_printing_url(self):
        return reverse(
            "react_views:r_tear_sheets:detail-view-for-print", kwargs={"id": self.pk}
        )

    def get_printing_url_no_list(self):
        return reverse(
            "react_views:r_tear_sheets:detail-view-for-print-list",
            kwargs={"id": self.pk},
        )

    def get_gbp_printing_url(self):
        return reverse(
            "react_views:r_gbp:detail-view-for-print", kwargs={"id": self.pk}
        )

    def get_gbp_printing_url_no_list(self):
        return reverse(
            "react_views:r_gbp:detail-view-for-print-list", kwargs={"id": self.pk}
        )

    def get_slug_title(self):
        return slugify(self.title)


class ImageCaption(models.Model):
    tear_sheet = models.ForeignKey(
        "TearSheet", blank=False, null=False, on_delete=models.CASCADE
    )
    order_no = models.IntegerField(
        help_text="The order number when this record appears with like records."
    )
    caption_title = models.CharField(
        help_text="Usually the position of the image being described.",
        blank=True,
        null=True,
        default="",
        max_length=1000,
    )
    caption = models.CharField(
        help_text="The image caption. Usually a product description.",
        blank=True,
        null=True,
        default="",
        max_length=1000,
    )

    def __str__(self):
        return f'Caption for tear sheet: "{self.tear_sheet}"'

    class Meta:
        ordering = ["order_no"]

    def return_file_name(self):
        split_up = self.file.url.split("/")
        return split_up[-1]

    def save(self, *args, **kwargs):
        self.tear_sheet.save()
        super(ImageCaption, self).save(*args, **kwargs)
