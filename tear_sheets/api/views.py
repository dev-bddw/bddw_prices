from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from price_records.models import FormulaPriceRecord, PriceRecord, TearSheetPriceRecord
from tear_sheets.models import (
    ImageCaption,
    TearSheet,
    TearSheetDetail,
    TearSheetFooterDetail,
    TearSheetFormatting,
)

from .serializers import (
    ImageCaptionSerializer,
    TearSheetDetailSerializer,
    TearSheetFooterDetailSerializer,
    TearSheetFormattingSerializer,
    TearSheetSerializer,
)


class TearSheetViewSet(viewsets.ModelViewSet):
    queryset = TearSheet.objects.all().order_by("title")
    serializer_class = TearSheetSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["title"]

    @action(detail=True, methods=["get"])
    def available_records(self, request, pk=None):
        """Get all available price records for this tearsheet's CatSeriesItem(s)"""
        tearsheet = self.get_object()
        cat_series_items = tearsheet.catseriesitem_set.all()

        if not cat_series_items.exists():
            return Response({"price_records": [], "formula_price_records": []})

        # Get all price records for these CatSeriesItems
        price_records = PriceRecord.objects.filter(
            cat_series_item__in=cat_series_items
        ).order_by("rule_display_1")
        formula_price_records = FormulaPriceRecord.objects.filter(
            cat_series_item__in=cat_series_items
        ).order_by("rule_display_1")

        from price_records.api.serializers import (
            FormulaPriceRecordSerializer,
            PriceRecordSerializer,
        )
        
        # Get existing selections to include status
        existing_selections = TearSheetPriceRecord.objects.filter(
            tear_sheet=tearsheet
        )
        pr_selection_map = {sel.price_record_id: sel for sel in existing_selections if sel.price_record_id}
        fpr_selection_map = {sel.formula_price_record_id: sel for sel in existing_selections if sel.formula_price_record_id}
        
        # Serialize with selection status
        pr_data = []
        for pr in price_records:
            pr_serialized = PriceRecordSerializer(pr).data
            selection = pr_selection_map.get(pr.id)
            pr_serialized['is_selected'] = selection.is_active if selection else False
            pr_serialized['selection_id'] = selection.id if selection else None
            pr_data.append(pr_serialized)
        
        fpr_data = []
        for fpr in formula_price_records:
            fpr_serialized = FormulaPriceRecordSerializer(fpr).data
            selection = fpr_selection_map.get(fpr.id)
            fpr_serialized['is_selected'] = selection.is_active if selection else False
            fpr_serialized['selection_id'] = selection.id if selection else None
            fpr_data.append(fpr_serialized)

        return Response(
            {
                "price_records": pr_data,
                "formula_price_records": fpr_data,
            }
        )

    @action(detail=True, methods=["get"])
    def selected_records(self, request, pk=None):
        """Get currently selected/active price records for this tearsheet"""
        tearsheet = self.get_object()
        selections = TearSheetPriceRecord.objects.filter(
            tear_sheet=tearsheet, is_active=True
        ).order_by("display_order")

        from price_records.api.serializers import TearSheetPriceRecordSerializer

        return Response(
            TearSheetPriceRecordSerializer(selections, many=True).data
        )

    @action(detail=True, methods=["post"])
    def select_records(self, request, pk=None):
        """Select which price records to display (bulk update is_active)"""
        tearsheet = self.get_object()
        price_record_ids = request.data.get("price_record_ids", [])
        formula_price_record_ids = request.data.get("formula_price_record_ids", [])

        # Get all CatSeriesItems for this tearsheet
        cat_series_items = tearsheet.catseriesitem_set.all()

        # Get all available records
        all_price_records = PriceRecord.objects.filter(
            cat_series_item__in=cat_series_items
        )
        all_formula_price_records = FormulaPriceRecord.objects.filter(
            cat_series_item__in=cat_series_items
        )

        # Deactivate all current selections
        TearSheetPriceRecord.objects.filter(tear_sheet=tearsheet).update(
            is_active=False
        )

        # Create/update selections for regular price records
        for pr_id in price_record_ids:
            try:
                pr = all_price_records.get(id=pr_id)
                tspr, created = TearSheetPriceRecord.objects.get_or_create(
                    tear_sheet=tearsheet,
                    price_record=pr,
                    defaults={"is_active": True, "display_order": 0},
                )
                if not created:
                    tspr.is_active = True
                    tspr.save()
            except PriceRecord.DoesNotExist:
                pass

        # Create/update selections for formula price records
        for fpr_id in formula_price_record_ids:
            try:
                fpr = all_formula_price_records.get(id=fpr_id)
                tspr, created = TearSheetPriceRecord.objects.get_or_create(
                    tear_sheet=tearsheet,
                    formula_price_record=fpr,
                    defaults={"is_active": True, "display_order": 0},
                )
                if not created:
                    tspr.is_active = True
                    tspr.save()
            except FormulaPriceRecord.DoesNotExist:
                pass

        return Response({"status": "success"})

    @action(detail=True, methods=["post"], url_path="toggle-record/(?P<record_id>[^/.]+)")
    def toggle_record(self, request, pk=None, record_id=None):
        """Toggle single record show/hide"""
        tearsheet = self.get_object()
        record_type = request.data.get("type")  # "price_record" or "formula_price_record"

        try:
            if record_type == "formula_price_record":
                tspr = TearSheetPriceRecord.objects.get(
                    tear_sheet=tearsheet, formula_price_record_id=record_id
                )
            else:
                tspr = TearSheetPriceRecord.objects.get(
                    tear_sheet=tearsheet, price_record_id=record_id
                )
            tspr.is_active = not tspr.is_active
            tspr.save()
            return Response({"is_active": tspr.is_active})
        except TearSheetPriceRecord.DoesNotExist:
            # Create new selection
            if record_type == "formula_price_record":
                try:
                    fpr = FormulaPriceRecord.objects.get(id=record_id)
                    tspr = TearSheetPriceRecord.objects.create(
                        tear_sheet=tearsheet,
                        formula_price_record=fpr,
                        is_active=True,
                        display_order=0,
                    )
                    return Response({"is_active": True})
                except FormulaPriceRecord.DoesNotExist:
                    return Response(
                        {"error": "Record not found"}, status=status.HTTP_404_NOT_FOUND
                    )
            else:
                try:
                    pr = PriceRecord.objects.get(id=record_id)
                    tspr = TearSheetPriceRecord.objects.create(
                        tear_sheet=tearsheet,
                        price_record=pr,
                        is_active=True,
                        display_order=0,
                    )
                    return Response({"is_active": True})
                except PriceRecord.DoesNotExist:
                    return Response(
                        {"error": "Record not found"}, status=status.HTTP_404_NOT_FOUND
                    )

    @action(detail=True, methods=["post"])
    def reorder_records(self, request, pk=None):
        """Reorder price records (update display_order)"""
        tearsheet = self.get_object()
        record_ids = request.data.get("record_ids", [])

        for index, record_id in enumerate(record_ids):
            TearSheetPriceRecord.objects.filter(
                tear_sheet=tearsheet, id=record_id
            ).update(display_order=index)

        return Response({"status": "success"})

    @action(detail=True, methods=["post"])
    def preserve_formatting(self, request, pk=None):
        """Save formatting snapshot"""
        tearsheet = self.get_object()
        formatting_data = request.data.get("formatting_data", {})

        formatting, created = TearSheetFormatting.objects.get_or_create(
            tear_sheet=tearsheet
        )
        formatting.formatting_data = formatting_data
        formatting.save()

        return Response(
            TearSheetFormattingSerializer(formatting).data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"])
    def restore_formatting(self, request, pk=None):
        """Restore formatting from snapshot"""
        tearsheet = self.get_object()

        try:
            formatting = TearSheetFormatting.objects.get(tear_sheet=tearsheet)
            # Restore formatting to tearsheet
            if "sdata" in formatting.formatting_data:
                tearsheet.sdata = formatting.formatting_data["sdata"]
            if "gbp_sdata" in formatting.formatting_data:
                tearsheet.gbp_sdata = formatting.formatting_data["gbp_sdata"]
            if "template" in formatting.formatting_data:
                tearsheet.template = formatting.formatting_data["template"]
            if "gbp_template" in formatting.formatting_data:
                tearsheet.gbp_template = formatting.formatting_data["gbp_template"]
            tearsheet.save()

            return Response({"status": "restored"})
        except TearSheetFormatting.DoesNotExist:
            return Response(
                {"error": "No formatting snapshot found"},
                status=status.HTTP_404_NOT_FOUND,
            )


class TearSheetDetailViewSet(viewsets.ModelViewSet):
    queryset = TearSheetDetail.objects.all().order_by("tear_sheet", "order")
    serializer_class = TearSheetDetailSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["tear_sheet__title", "name", "details"]


class TearSheetFooterDetailViewSet(viewsets.ModelViewSet):
    queryset = TearSheetFooterDetail.objects.all().order_by("tear_sheet", "order")
    serializer_class = TearSheetFooterDetailSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["tear_sheet__title", "name", "details"]


class ImageCaptionViewSet(viewsets.ModelViewSet):
    queryset = ImageCaption.objects.all().order_by("tear_sheet", "order_no")
    serializer_class = ImageCaptionSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["tear_sheet__title", "caption_title", "caption"]
