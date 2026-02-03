from rest_framework import serializers

from products.models import Category, CatSeriesItem, Item, Series


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "order", "pricelist_ignore"]
        read_only_fields = ["id"]


class SeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Series
        fields = ["id", "name"]
        read_only_fields = ["id"]


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ["id", "name"]
        read_only_fields = ["id"]


class CatSeriesItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source="category", write_only=True
    )
    series = SeriesSerializer(read_only=True)
    series_id = serializers.PrimaryKeyRelatedField(
        queryset=Series.objects.all(), source="series", write_only=True
    )
    item = ItemSerializer(read_only=True)
    item_id = serializers.PrimaryKeyRelatedField(
        queryset=Item.objects.all(), source="item", write_only=True
    )

    class Meta:
        model = CatSeriesItem
        fields = [
            "id",
            "category",
            "category_id",
            "series",
            "series_id",
            "item",
            "item_id",
            "cat_order",
            "series_order",
            "item_order",
            "opt_series_item_display",
            "formula",
            "tear_sheet",
            "formula_tear_sheet",
        ]
        read_only_fields = ["id"]
