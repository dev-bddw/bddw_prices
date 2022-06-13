from django.contrib import admin

from .models import ImageCaption, TearSheet, TearSheetDetail, TearSheetFooterDetail


class TearsheetAdmin(admin.ModelAdmin):
    pass


class TearsheetDetailAdmin(admin.ModelAdmin):
    pass


class ImageCaptionAdmin(admin.ModelAdmin):
    pass


class TearSheetFooterDetailAdmin(admin.ModelAdmin):
    pass


admin.site.register(ImageCaption, ImageCaptionAdmin)
admin.site.register(TearSheet, TearsheetAdmin)
admin.site.register(TearSheetDetail, TearsheetDetailAdmin)
admin.site.register(TearSheetFooterDetail, TearSheetFooterDetailAdmin)
