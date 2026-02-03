from rest_framework import serializers

from price_records.models import (
    FormulaPriceRecord,
    PriceRecord,
    TearSheetPriceRecord,
)


class PriceRecordSerializer(serializers.ModelSerializer):
    cat_series_item_name = serializers.CharField(
        source="cat_series_item.__str__", read_only=True
    )

    class Meta:
        model = PriceRecord
        fields = [
            "id",
            "cat_series_item",
            "cat_series_item_name",
            "rule_type",
            "rule_display_1",
            "rule_display_2",
            "list_price",
            "net_price",
            "gbp_price",
            "gbp_trade",
            "gbp_price_no_vat",
            "gbp_trade_no_vat",
            "order",
            "bin_id",
            "is_surcharge",
            "man_order",
        ]
        read_only_fields = ["id", "net_price"]


class FormulaPriceRecordSerializer(serializers.ModelSerializer):
    cat_series_item_name = serializers.CharField(
        source="cat_series_item.__str__", read_only=True
    )

    class Meta:
        model = FormulaPriceRecord
        fields = [
            "id",
            "cat_series_item",
            "cat_series_item_name",
            "rule_type",
            "rule_display_1",
            "rule_display_2",
            "list_price",
            "net_price",
            "gbp_price",
            "gbp_trade",
            "gbp_price_no_vat",
            "gbp_trade_no_vat",
            "order",
            "depth",
            "length",
            "width",
            "diameter",
            "height",
            "footboard_height",
            "headboard_height",
            "headboard_width",
            "seat_fabric_yardage",
            "seat_back_height",
            "seat_height",
            "inset",
        ]
        read_only_fields = ["id", "list_price", "net_price"]


class TearSheetPriceRecordSerializer(serializers.ModelSerializer):
    price_record = PriceRecordSerializer(read_only=True)
    price_record_id = serializers.PrimaryKeyRelatedField(
        queryset=PriceRecord.objects.all(),
        source="price_record",
        write_only=True,
        required=False,
        allow_null=True,
    )
    formula_price_record = FormulaPriceRecordSerializer(read_only=True)
    formula_price_record_id = serializers.PrimaryKeyRelatedField(
        queryset=FormulaPriceRecord.objects.all(),
        source="formula_price_record",
        write_only=True,
        required=False,
        allow_null=True,
    )

    class Meta:
        model = TearSheetPriceRecord
        fields = [
            "id",
            "tear_sheet",
            "price_record",
            "price_record_id",
            "formula_price_record",
            "formula_price_record_id",
            "display_order",
            "is_active",
        ]
        read_only_fields = ["id"]
