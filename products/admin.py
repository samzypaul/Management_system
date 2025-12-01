from django.contrib import admin
from .models import Product, StockTransaction


# Inline transactions inside Product admin
class StockTransactionInline(admin.TabularInline):
    model = StockTransaction
    extra = 1  # show one empty row by default
    readonly_fields = ("timestamp",)  # timestamp should not be editable


class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "quantity","currency")
    search_fields = ("name", "category")
    inlines = [StockTransactionInline]  # show transactions inside product page


class StockTransactionAdmin(admin.ModelAdmin):
    list_display = ("product", "transaction_type", "quantity", "timestamp", "note")
    list_filter = ("transaction_type", "timestamp")
    search_fields = ("product__name", "note")


# Register models with their admin configs
admin.site.register(Product, ProductAdmin)
admin.site.register(StockTransaction, StockTransactionAdmin)
