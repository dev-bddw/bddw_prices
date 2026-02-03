from django.db import models


class Category(models.Model):
    name = models.CharField(unique=True, blank=True, null=True, max_length=200)
    order = models.IntegerField(blank=True, null=True)
    pricelist_ignore = models.BooleanField(
        default=False,
        help_text="If selected (true) rules for this category will not show up in pricelist",
    )

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["order"]

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        for obj in CatSeriesItem.objects.filter(category=self):
            if (obj.cat_order is not None) and (obj.cat_order != ""):
                self.order = obj.cat_order
                break

        super(Category, self).save(*args, **kwargs)


class Series(models.Model):
    class TearSheetGrouping(models.TextChoices):
        BY_ITEM = "by_item", "By Item (one tearsheet per Category-Series-Item)"
        BY_SERIES = "by_series", "By Series (one tearsheet per Category-Series)"

    name = models.CharField(unique=True, blank=True, null=True, max_length=200)
    tearsheet_grouping = models.CharField(
        choices=TearSheetGrouping.choices,
        default=TearSheetGrouping.BY_ITEM,
        max_length=20,
        help_text="Controls whether tearsheets are grouped by individual items or by the entire series",
    )

    class Meta:
        verbose_name_plural = "Series"

    def __str__(self):
        return f"{self.name}"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Store the original tearsheet_grouping value to detect changes
        self._original_tearsheet_grouping = self.tearsheet_grouping
    
    def refresh_from_db(self, using=None, fields=None):
        """Override to update _original_tearsheet_grouping after refresh"""
        super().refresh_from_db(using=using, fields=fields)
        self._original_tearsheet_grouping = self.tearsheet_grouping
    
    def save(self, *args, **kwargs):
        # Check if tearsheet_grouping has changed
        tearsheet_grouping_changed = (
            self.pk is not None and  # Only reorganize if this is an existing instance
            self._original_tearsheet_grouping != self.tearsheet_grouping
        )
        
        # Save the model first
        super().save(*args, **kwargs)
        
        # Reorganize tearsheets if the grouping changed
        if tearsheet_grouping_changed:
            self._reorganize_tearsheets()
    
    def _reorganize_tearsheets(self):
        """
        Reorganize tearsheets for this series based on the current tearsheet_grouping setting.
        """
        from django.db import transaction
        
        with transaction.atomic():
            if self.tearsheet_grouping == self.TearSheetGrouping.BY_SERIES.value:
                self._reorganize_to_series_grouping()
            else:
                self._reorganize_to_item_grouping()
    
    def _reorganize_to_series_grouping(self):
        """Merge item-level tearsheets into series-level tearsheets"""
        from tear_sheets.models import TearSheet
        from price_records.models import PriceRecord, FormulaPriceRecord, TearSheetPriceRecord
        
        # Group CatSeriesItems by Category
        categories = CatSeriesItem.objects.filter(series=self).values_list('category', flat=True).distinct()
        
        for category_id in categories:
            category_csis = CatSeriesItem.objects.filter(series=self, category_id=category_id)
            category = category_csis.first().category
            
            # Determine the target tearsheet title
            target_title = f"{category} - {self}"
            
            # Get or create the series-level tearsheet
            target_tearsheet, created = TearSheet.objects.get_or_create(
                title=target_title,
                defaults={
                    'template': 'B',
                    'gbp_template': 'C',
                }
            )
            
            # Collect all price records from all items in this category-series
            all_price_records = []
            all_formula_price_records = []
            old_tearsheets = set()
            
            for csi in category_csis:
                # Collect old tearsheet for cleanup
                if csi.tear_sheet:
                    old_tearsheets.add(csi.tear_sheet)
                
                # Link CSI to target tearsheet
                csi.tear_sheet = target_tearsheet
                csi.save()
                
                # Collect price records
                all_price_records.extend(PriceRecord.objects.filter(cat_series_item=csi))
                all_formula_price_records.extend(FormulaPriceRecord.objects.filter(cat_series_item=csi))
            
            # Create TearSheetPriceRecord entries for all price records
            # If tearsheet is new, make records visible; if existing, preserve existing state or default to visible
            for pr in all_price_records:
                tspr, tspr_created = TearSheetPriceRecord.objects.get_or_create(
                    tear_sheet=target_tearsheet,
                    price_record=pr,
                    defaults={
                        'display_order': pr.order if pr.order else 0,
                        'is_active': created,  # True for new tearsheets, True for reorganization
                    }
                )
                # If this is a new TearSheetPriceRecord on an existing tearsheet, make it visible (reorganization case)
                if not created and tspr_created:
                    tspr.is_active = True
                    tspr.save()
            
            for fpr in all_formula_price_records:
                tspr, tspr_created = TearSheetPriceRecord.objects.get_or_create(
                    tear_sheet=target_tearsheet,
                    formula_price_record=fpr,
                    defaults={
                        'display_order': fpr.order if fpr.order else 0,
                        'is_active': created,  # True for new tearsheets, True for reorganization
                    }
                )
                # If this is a new TearSheetPriceRecord on an existing tearsheet, make it visible (reorganization case)
                if not created and tspr_created:
                    tspr.is_active = True
                    tspr.save()
            
            # Clean up old tearsheets that are no longer needed
            for old_ts in old_tearsheets:
                if old_ts != target_tearsheet:
                    # Check if this tearsheet has any other CatSeriesItems
                    other_csis = CatSeriesItem.objects.filter(tear_sheet=old_ts).exclude(
                        series=self, category_id=category_id
                    )
                    if not other_csis.exists():
                        # Delete TearSheetPriceRecords for this tearsheet
                        TearSheetPriceRecord.objects.filter(tear_sheet=old_ts).delete()
                        old_ts.delete()
    
    def _reorganize_to_item_grouping(self):
        """Split series-level tearsheets into item-level tearsheets"""
        from tear_sheets.models import TearSheet
        from price_records.models import PriceRecord, FormulaPriceRecord, TearSheetPriceRecord
        
        # Get all CatSeriesItems for this series
        csis = CatSeriesItem.objects.filter(series=self)
        
        for csi in csis:
            # Determine the target tearsheet title
            target_title = f"{csi.category} - {csi.series} - {csi.item}"
            
            # Get or create the item-level tearsheet
            target_tearsheet, created = TearSheet.objects.get_or_create(
                title=target_title,
                defaults={
                    'template': 'B',
                    'gbp_template': 'C',
                }
            )
            
            # Link CSI to target tearsheet
            old_tearsheet = csi.tear_sheet
            csi.tear_sheet = target_tearsheet
            csi.save()
            
            # Get price records for this specific CSI
            price_records = PriceRecord.objects.filter(cat_series_item=csi)
            formula_price_records = FormulaPriceRecord.objects.filter(cat_series_item=csi)
            
            # Create TearSheetPriceRecord entries
            # If tearsheet is new, make records visible; if existing, preserve existing state or default to visible
            for pr in price_records:
                tspr, tspr_created = TearSheetPriceRecord.objects.get_or_create(
                    tear_sheet=target_tearsheet,
                    price_record=pr,
                    defaults={
                        'display_order': pr.order if pr.order else 0,
                        'is_active': created,  # True for new tearsheets, True for reorganization
                    }
                )
                # If this is a new TearSheetPriceRecord on an existing tearsheet, make it visible (reorganization case)
                if not created and tspr_created:
                    tspr.is_active = True
                    tspr.save()
            
            for fpr in formula_price_records:
                tspr, tspr_created = TearSheetPriceRecord.objects.get_or_create(
                    tear_sheet=target_tearsheet,
                    formula_price_record=fpr,
                    defaults={
                        'display_order': fpr.order if fpr.order else 0,
                        'is_active': created,  # True for new tearsheets, True for reorganization
                    }
                )
                # If this is a new TearSheetPriceRecord on an existing tearsheet, make it visible (reorganization case)
                if not created and tspr_created:
                    tspr.is_active = True
                    tspr.save()
            
            # Clean up old tearsheet if it was series-level and no longer needed
            if old_tearsheet and old_tearsheet != target_tearsheet:
                # Check if this tearsheet has any other CatSeriesItems
                other_csis = CatSeriesItem.objects.filter(tear_sheet=old_tearsheet).exclude(pk=csi.pk)
                if not other_csis.exists():
                    # Delete TearSheetPriceRecords for this tearsheet
                    TearSheetPriceRecord.objects.filter(tear_sheet=old_tearsheet).delete()
                    old_tearsheet.delete()


class Item(models.Model):
    name = models.CharField(unique=True, blank=True, null=True, max_length=200)

    class Meta:
        verbose_name_plural = "Items"

    def __str__(self):
        return f"{self.name}"


class CatSeriesItem(models.Model):
    category = models.ForeignKey(
        "products.Category", blank=False, null=False, on_delete=models.DO_NOTHING
    )
    series = models.ForeignKey(
        "products.Series", blank=False, null=False, on_delete=models.DO_NOTHING
    )
    item = models.ForeignKey(
        "products.Item", blank=False, null=False, on_delete=models.DO_NOTHING
    )

    cat_order = models.IntegerField(blank=True, null=True)
    series_order = models.IntegerField(blank=True, null=True)
    item_order = models.IntegerField(blank=True, null=True)

    opt_series_item_display = models.CharField(
        blank=True,
        null=True,
        default=None,
        help_text="Display alternate series item string?",
        max_length=200,
    )

    formula = models.CharField(
        blank=True,
        null=True,
        default=None,
        help_text="The string version of the formula",
        max_length=200,
    )
    tear_sheet = models.ForeignKey(
        "tear_sheets.TearSheet", blank=True, null=True, on_delete=models.SET_NULL
    )

    formula_tear_sheet = models.ForeignKey(
        "formula_tear_sheets.FormulaTearSheet",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    def return_series_item(self):
        return (
            f"{self.series} {self.item}"
            if self.opt_series_item_display is None
            else self.opt_series_item_display
        )

    def save(self, *args, **kwargs):
        # roundabout way of ensuring unique for cat-series-item fk's
        try:
            item = CatSeriesItem.objects.get(
                category=self.category, series=self.series, item=self.item
            )
            if item.pk == self.pk:
                super(CatSeriesItem, self).save(*args, **kwargs)
            else:
                raise ValueError("This Category Series Item already exists")

        except CatSeriesItem.DoesNotExist:
            super(CatSeriesItem, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.category} - {self.series} - {self.item}"

    def return_translation(self):
        try:
            f = self.formula.replace("[", "").replace("]", "")

            import re

            formula = re.sub(r"([a-z])\s([a-z])", "\\1_\\2", f)

            return formula

        except AttributeError:
            pass

    def return_price_records(self):
        if self.formula is None or "":
            from price_records.models import PriceRecord

            return PriceRecord.objects.filter(cat_series_item_id=self.pk)
        else:
            from price_records.models import FormulaPriceRecord

            return FormulaPriceRecord.objects.filter(cat_series_item_id=self.pk)

    def has_formula(self):
        return True if self.formula not in ["", None] else False

    class Meta:
        verbose_name = "Category Series Item"
        verbose_name_plural = "Category Series Items"
        ordering = ["cat_order", "series_order", "item_order"]
