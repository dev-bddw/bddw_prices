from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from products.models import Category, CatSeriesItem, Item, Series

from .serializers import (
    CatSeriesItemSerializer,
    CategorySerializer,
    ItemSerializer,
    SeriesSerializer,
)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["name"]


class SeriesViewSet(viewsets.ModelViewSet):
    queryset = Series.objects.all().order_by("name")
    serializer_class = SeriesSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["name"]


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all().order_by("name")
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["name"]


class CatSeriesItemViewSet(viewsets.ModelViewSet):
    queryset = CatSeriesItem.objects.all().order_by(
        "category__name", "series__name", "item__name"
    )
    serializer_class = CatSeriesItemSerializer
    permission_classes = [IsAuthenticated]
    search_fields = [
        "category__name",
        "series__name",
        "item__name",
        "opt_series_item_display",
    ]
