from django.contrib import admin
from django.utils.html import format_html
from django.utils.text import Truncator

from .models import Category, CategoryIcon, Tag, Specification, Product, SpecificationValue, ProductImage, Review, Sale


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("pk", "avatar_thumbnail", "title", "is_active", "parent", "favourite")
    list_display_links = ("pk", "title")
    ordering = ["pk"]
    list_filter = ["is_active", "favourite"]
    search_fields = ["title"]

    @admin.display(description="Parent Category")
    def parent(self, obj):
        return obj.parent.title if obj.parent else None

    @admin.display(description="Avatar")
    def avatar_thumbnail(self, obj):
        return format_html(
            '<div style="display: flex; align-items: center; justify-content: center;">'
            '   <a href="{0}" target="_blank">'
            '       <img src="{0}" height="50" style="border-radius: 10%">'
            '   </a>'
            '</div>',
            obj.image.src.url
        )


@admin.register(CategoryIcon)
class CategoryIconAdmin(admin.ModelAdmin):
    list_display = ("pk", "avatar_thumbnail", "src", "alt", "category_title")
    list_display_links = ("pk", "avatar_thumbnail", "src")
    ordering = ["pk"]

    @admin.display(description="Category Title")
    def category_title(self, obj):
        return obj.category.title if obj.category else None

    @admin.display(description="Avatar")
    def avatar_thumbnail(self, obj):
        return format_html(
            '<div style="display: flex; align-items: center; justify-content: center;">'
            '   <a href="{0}" target="_blank">'
            '       <img src="{0}" height="50" style="border-radius: 10%">'
            '   </a>'
            '</div>',
            obj.src.url
        )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("pk", "name")
    list_display_links = ("pk", "name")
    ordering = ["pk"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "title",
        "price",
        "category_title",
        "is_active",
        "count",
        "short_description",
        "freeDelivery",
        "limited_edition",
    )
    list_display_links = ("pk", "title")
    ordering = ["pk"]
    list_filter = ["category", "is_active", "freeDelivery", "limited_edition"]
    search_fields = ["title", "description", "fullDescription"]

    fieldsets = (
        (None, {
            "fields": ("title", "price", "count", "category", "is_active", "tags")
        }),
        ("Description", {
            "fields": ("description", "fullDescription", "freeDelivery", "limited_edition"),
        }),
    )

    @admin.display(description="Category")
    def category_title(self, obj):
        return obj.category.title if obj.category else None

    @admin.display(description="Description")
    def short_description(self, obj):
        truncated_description = Truncator(obj.description).chars(48)
        return format_html(f'<span title="{obj.description}">{truncated_description}</span>')


@admin.register(Specification)
class SpecificationAdmin(admin.ModelAdmin):
    list_display = ("pk", "name")
    list_display_links = ("pk", "name")
    ordering = ["pk"]


@admin.register(SpecificationValue)
class SpecificationValueAdmin(admin.ModelAdmin):
    list_display = ("pk", "value", "specification_name", "product_title")
    list_display_links = ("pk", "value")
    ordering = ["pk"]

    @admin.display(description="Specification")
    def specification_name(self, obj):
        return obj.specification.name if obj.specification else None

    @admin.display(description="Product")
    def product_title(self, obj):
        return obj.product.title if obj.product else None


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("pk", "image_thumbnail", "alt", "product_title")
    list_display_links = ("pk", "image_thumbnail")
    ordering = ["pk"]

    @admin.display(description="Product")
    def product_title(self, obj):
        return obj.product.title if obj.product else None

    @admin.display(description="Preview")
    def image_thumbnail(self, obj):
        return format_html(
            '<div style="display: flex; align-items: center; justify-content: center;">'
            '   <img src="{}" style="border-radius: 10%; max-width: 100px; max-height: 50px;">'
            '</div>',
            obj.src.url
        )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("pk", "author", "email", "text", "product_title", "date", "rate")
    list_display_links = ("pk", "author")
    ordering = ["pk"]

    @admin.display(description="Product")
    def product_title(self, obj):
        return obj.product.title if obj.product else None


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ("pk", "product_image", "product_title", "salePrice", "dateFrom", "dateTo")
    list_display_links = ("pk", "product_title")
    ordering = ["pk"]

    @admin.display(description="Product")
    def product_title(self, obj):
        return obj.product.title if obj.product else None

    @admin.display(description="Product Image")
    def product_image(self, obj):
        if obj.product.images.exists():
            image = obj.product.images.first()
            return format_html(
                '<div style="display: flex; align-items: center; justify-content: center;">'
                '   <a href="{0}" target="_blank">'
                '       <img src="{0}" height="50" style="border-radius: 10%">'
                '   </a>'
                '</div>',
                image.src.url
            )
        return None
