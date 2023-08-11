from app.admin import admin
from app.admin import ModelAdmin
from products.models import Category
from products.models import Image
from products.models import Product
from products.models import ProductOption
from products.models import ProductVariant
from products.models import Review


class ImageInline(admin.TabularInline):
    model = Image
    extra = 1


class OptionInline(admin.StackedInline):
    model = ProductOption
    extra = 1


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    inlines = [
        OptionInline,
        ImageInline,
    ]
    list_display = ("name", "get_price_range", "short_description", "views")
    list_filter = ("category", "created", "modified", "available")
    search_fields = ("name", "short_description", "description", "information")
    date_hierarchy = "created"
    ordering = ["-created"]

    @admin.display(
        description="price",
    )
    def get_price_range(self, obj: Product) -> str:
        return obj.price_range


@admin.register(ProductVariant)
class ProductVariantAdmin(ModelAdmin):
    list_display = ("product", "option", "actual_price", "price", "discount", "quantity")
    search_fields = ("product", "option")
    list_filter = ("available", "created", "modified")
    ordering = ["-created"]


@admin.register(Review)
class ReviewAdmin(ModelAdmin):
    list_display = ("rating", "product", "user", "comment")
    search_fields = ("product", "user", "comment")
    list_filter = ("rating", "created", "modified")
    ordering = ["-created"]


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name", "description")
    list_filter = ("name", "created", "modified")
    exclude = ("slug",)
