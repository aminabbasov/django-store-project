from app.admin import admin, ModelAdmin

from products import models


class ImageInline(admin.StackedInline):
    model = models.Image
    extra = 1

@admin.register(models.Product)
class ProductAdmin(ModelAdmin):
    inlines = [
        ImageInline,
    ]
    
    list_display = ('name', 'get_actual_price', 'color', 'size')
    list_filter = ('category', 'color', 'size')
    search_fields = ('name', 'short_description', 'description', 'information')
    # raw_id_fields = ('category',)
    date_hierarchy = 'created'
    ordering = ['-created']
    
    @admin.display(
        # ordering='price',
        description='actual_price',
    )
    def get_actual_price(self, obj):
        if obj.discount:
            return round(obj.price - ((obj.price * obj.discount) / 100), 2)
        return obj.price


@admin.register(models.Review)
class ReviewAdmin(ModelAdmin):
    ...


@admin.register(models.Category)
class CategoryAdmin(ModelAdmin):
    # prepopulated_fields = {"slug": ("category",)}
    exclude = ('slug',)
