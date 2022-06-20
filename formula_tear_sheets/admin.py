from allauth.socialaccount.models import SocialAccount, SocialApp, SocialToken
from django.contrib import admin

from .models import (
    FormulaImageCaption,
    FormulaTearSheet,
    FormulaTearSheetDetail,
    FormulaTearSheetFooterDetail,
)


class FormulaTearsheetAdmin(admin.ModelAdmin):
    pass


class FormulaTearsheetDetailAdmin(admin.ModelAdmin):
    pass


class FormulaImageCaptionAdmin(admin.ModelAdmin):
    pass


class FormulaTearSheetFooterDetailAdmin(admin.ModelAdmin):
    pass


admin.site.register(FormulaImageCaption, FormulaImageCaptionAdmin)
admin.site.register(FormulaTearSheet, FormulaTearsheetAdmin)
admin.site.register(FormulaTearSheetDetail, FormulaTearsheetDetailAdmin)
admin.site.register(FormulaTearSheetFooterDetail, FormulaTearSheetFooterDetailAdmin)


admin.site.unregister(SocialToken)
admin.site.unregister(SocialAccount)
admin.site.unregister(SocialApp)
