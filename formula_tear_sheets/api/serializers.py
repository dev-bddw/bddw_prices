from rest_framework import serializers

from formula_tear_sheets.models import (
    FormulaImageCaption,
    FormulaTearSheet,
    FormulaTearSheetDetail,
    FormulaTearSheetFooterDetail,
)


class FormulaTearSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormulaTearSheet
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


class FormulaTearSheetDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormulaTearSheetDetail
        fields = ["id", "tear_sheet", "name", "details", "order"]
        read_only_fields = ["id"]


class FormulaTearSheetFooterDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormulaTearSheetFooterDetail
        fields = ["id", "tear_sheet", "name", "details", "order"]
        read_only_fields = ["id"]


class FormulaImageCaptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormulaImageCaption
        fields = ["id", "tear_sheet", "order_no", "caption_title", "caption"]
        read_only_fields = ["id"]
