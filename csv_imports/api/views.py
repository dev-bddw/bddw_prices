from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from csv_imports.helpers import process_records


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def inventory_sync(request):
    """
    Bulk sync from BIN inventory system.
    Accepts JSON payload matching CSV structure.
    Uses bin_id to match existing records.
    Updates prices while preserving tearsheet selections.
    """
    records = request.data.get("records", [])

    if not records:
        return Response(
            {"error": "No records provided"}, status=status.HTTP_400_BAD_REQUEST
        )

    # Transform API payload to match process_records format
    empty_values = [0, "0", ""]
    transformed_records = []

    for record in records:
        transformed_record = {
            "category": record.get("category", ""),
            "series": record.get("series", ""),
            "item": record.get("item", ""),
            "is_tearsheet": record.get("tearsheet") not in empty_values,
            "is_pricelist": record.get("price_list") not in empty_values,
            "is_formula": record.get("formula") not in empty_values,
            "formula": record.get("formula", ""),
            "bin_id": record.get("bin_id", ""),
            "rule_type": record.get("rule_type", ""),
            "list_price": record.get("list_price", "")
            if record.get("list_price", "") != ""
            else record.get("surcharge", ""),
            "ts_rule_display_1": record.get("ts_rule_display_1", ""),
            "ts_rule_display_2": record.get("ts_rule_display_2", ""),
            "pl_rule_display_1": record.get("pl_rule_display_1", ""),
            "pl_rule_display_2": record.get("pl_rule_display_2", ""),
            "order": record.get("order", 1),
            "surcharge": False if record.get("surcharge", "") == "" else True,
            "gbp_price": record.get("gbp", ""),
            "gbp_price_no_vat": record.get("gbp_minus_vat", ""),
            "gbp_trade_no_vat": record.get("gbp_trade_minus_vat", ""),
            "gbp_trade": record.get("gbp_trade", ""),
        }
        transformed_records.append(transformed_record)

    # Process records (this updates prices but preserves tearsheet selections)
    report = process_records(transformed_records)

    # Count stats
    created_count = sum(1 for r in report if r.get("status") == "created")
    updated_count = sum(1 for r in report if r.get("status") == "updated")
    errors = [r for r in report if r.get("status") == "Failed"]

    return Response(
        {
            "status": "success",
            "summary": {
                "total": len(report),
                "created": created_count,
                "updated": updated_count,
                "errors": len(errors),
            },
            "report": report,
        },
        status=status.HTTP_200_OK,
    )
