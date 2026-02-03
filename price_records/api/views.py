from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from price_records.models import (
    FormulaPriceRecord,
    PriceRecord,
    TearSheetPriceRecord,
)

from .serializers import (
    FormulaPriceRecordSerializer,
    PriceRecordSerializer,
    TearSheetPriceRecordSerializer,
)


class PriceRecordViewSet(viewsets.ModelViewSet):
    queryset = PriceRecord.objects.all().order_by(
        "cat_series_item__category__name", "rule_display_1"
    )
    serializer_class = PriceRecordSerializer
    permission_classes = [IsAuthenticated]
    search_fields = [
        "cat_series_item__category__name",
        "cat_series_item__series__name",
        "cat_series_item__item__name",
        "rule_display_1",
        "rule_display_2",
    ]


class FormulaPriceRecordViewSet(viewsets.ModelViewSet):
    queryset = FormulaPriceRecord.objects.all().order_by(
        "cat_series_item__category__name", "rule_display_1"
    )
    serializer_class = FormulaPriceRecordSerializer
    permission_classes = [IsAuthenticated]
    search_fields = [
        "cat_series_item__category__name",
        "cat_series_item__series__name",
        "cat_series_item__item__name",
        "rule_display_1",
        "rule_display_2",
    ]


class TearSheetPriceRecordViewSet(viewsets.ModelViewSet):
    queryset = TearSheetPriceRecord.objects.all().order_by(
        "tear_sheet", "display_order"
    )
    serializer_class = TearSheetPriceRecordSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["tear_sheet__title"]
