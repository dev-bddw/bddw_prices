from django.db import models
from django.urls import reverse


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


class TearSheetDetail(Detail):
    pass


class TearSheetFooterDetail(Detail):
    pass


class TearSheet(models.Model):
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

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("tearsheets:detail", kwargs={"pk": self.pk})

    def get_edit_url(self):
        return reverse("tearsheets:edit", kwargs={"pk": self.pk})

    def get_printing_url(self):
        return reverse("tearsheets:detail-view-for-print", kwargs={"pk": self.pk})


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
