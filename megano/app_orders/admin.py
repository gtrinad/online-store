from django.contrib import admin

from app_orders.models import ProductsInOrder, Order


class ProductsInOrderInline(admin.TabularInline):
    model = ProductsInOrder
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("pk", "createdAt", "user", "totalCost", "status")
    list_filter = ("status", "createdAt")
    search_fields = ("user__username", "user__email", "city", "address")
    inlines = [ProductsInOrderInline]

    fieldsets = (
        (
            "General Information",
            {"fields": ("user", "deliveryType", "paymentType", "totalCost", "status")},
        ),
        ("Address Information", {"fields": ("city", "address")}),
        ("Products", {"fields": ("products",)}),
    )


@admin.register(ProductsInOrder)
class ProductsInOrderAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "count")
    list_filter = ("order__status",)
    search_fields = (
        "order__user__username",
        "product__title",
        "order__city",
        "order__address",
    )
