from django.contrib import admin

from .models import Category, CatSeriesItem, Item, Series


class CatSeriesItemAdmin(admin.ModelAdmin):
    search_fields = ["series__name", "category__name", "item__name"]
    list_per_page = 10000


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_per_page = 10000


class ItemAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_per_page = 10000


class SeriesAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_per_page = 10000


admin.site.register(CatSeriesItem, CatSeriesItemAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Series, SeriesAdmin)
