from django.contrib import admin

from .models import Category, CatSeriesItem, Item, Series


class CatSeriesItemAdmin(admin.ModelAdmin):
    pass


class CategoryAdmin(admin.ModelAdmin):
    pass


class ItemAdmin(admin.ModelAdmin):
    pass


class SeriesAdmin(admin.ModelAdmin):
    pass


admin.site.register(CatSeriesItem, CatSeriesItemAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Series, SeriesAdmin)
