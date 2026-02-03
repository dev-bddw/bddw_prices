from rest_framework import serializers

from tear_sheets.models import (
    ImageCaption,
    TearSheet,
    TearSheetDetail,
    TearSheetFooterDetail,
    TearSheetFormatting,
)


class TearSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = TearSheet
        fields = [
            "id",
            "title",
            "image",
            "template",
            "gbp_template",
            "sdata",
            "gbp_sdata",
            "footer_space",
            "updated_on",
        ]
        read_only_fields = ["id", "updated_on"]


class TearSheetDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TearSheetDetail
        fields = ["id", "tear_sheet", "name", "details", "order"]
        read_only_fields = ["id"]


class TearSheetFooterDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TearSheetFooterDetail
        fields = ["id", "tear_sheet", "name", "details", "order"]
        read_only_fields = ["id"]


class ImageCaptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageCaption
        fields = ["id", "tear_sheet", "order_no", "caption_title", "caption"]
        read_only_fields = ["id"]


class TearSheetFormattingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TearSheetFormatting
        fields = ["id", "tear_sheet", "last_updated", "formatting_data"]
        read_only_fields = ["id", "last_updated"]
