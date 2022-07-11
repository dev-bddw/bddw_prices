from django.db import models
from django.urls import reverse


def image_upload_to(instance, filename):
    return f"tear_sheet_images/{instance.title}/{filename}"


class FormulaTearSheet(models.Model):
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
        return reverse("formula_tearsheets:detail", kwargs={"pk": self.pk})

    def get_edit_url(self):
        return reverse("formula_tearsheets:edit", kwargs={"pk": self.pk})

    def get_printing_url(self):
        return reverse(
            "formula_tearsheets:detail-view-for-print", kwargs={"pk": self.pk}
        )


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
