from app.admin import admin, ModelAdmin

from products.models import Product, ProductOption, ProductVariant, Image, Category, Review


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


@admin.register(ProductVariant)
class ProductVariantAdmin(ModelAdmin):
    ...
    
    # list_display = ('name', 'get_actual_price', 'color', 'size')
    # list_filter = ('category', 'color', 'size')
    # search_fields = ('name', 'short_description', 'description', 'information')
    # # raw_id_fields = ('category',)
    # date_hierarchy = 'created'
    # ordering = ['-created']
    
    # @admin.display(
    #     # ordering='price',
    #     description='actual_price',
    # )
    # def get_actual_price(self, obj):
    #     if obj.discount:
    #         return round(obj.price - ((obj.price * obj.discount) / 100), 2)
    #     return obj.price


@admin.register(Review)
class ReviewAdmin(ModelAdmin):
    ...


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    # prepopulated_fields = {"slug": ("category",)}
    exclude = ('slug',)
