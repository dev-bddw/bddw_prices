from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from formula_tear_sheets.models import (
    FormulaImageCaption,
    FormulaTearSheet,
    FormulaTearSheetDetail,
    FormulaTearSheetFooterDetail,
)

from .serializers import (
    FormulaImageCaptionSerializer,
    FormulaTearSheetDetailSerializer,
    FormulaTearSheetFooterDetailSerializer,
    FormulaTearSheetSerializer,
)


class FormulaTearSheetViewSet(viewsets.ModelViewSet):
    queryset = FormulaTearSheet.objects.all().order_by("title")
    serializer_class = FormulaTearSheetSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["title"]


class FormulaTearSheetDetailViewSet(viewsets.ModelViewSet):
    queryset = FormulaTearSheetDetail.objects.all().order_by("tear_sheet", "order")
    serializer_class = FormulaTearSheetDetailSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["tear_sheet__title", "name", "details"]


class FormulaTearSheetFooterDetailViewSet(viewsets.ModelViewSet):
    queryset = FormulaTearSheetFooterDetail.objects.all().order_by(
        "tear_sheet", "order"
    )
    serializer_class = FormulaTearSheetFooterDetailSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["tear_sheet__title", "name", "details"]


class FormulaImageCaptionViewSet(viewsets.ModelViewSet):
    queryset = FormulaImageCaption.objects.all().order_by("tear_sheet", "order_no")
    serializer_class = FormulaImageCaptionSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["tear_sheet__title", "caption_title", "caption"]
