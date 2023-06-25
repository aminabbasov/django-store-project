from app.admin import admin, ModelAdmin

from checkout import models


class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    raw_id_fields = ['product']

@admin.register(models.Order)
class OrderAdmin(ModelAdmin):
    inlines = [
        OrderItemInline
    ]
    
    list_display = (
        'id', 'first_name', 'last_name', 'email',
        'address_line_1', 'zip_code', 'city', 'paid',
        'created', 'updated'
    )
    list_filter = ('paid', 'created', 'updated')
