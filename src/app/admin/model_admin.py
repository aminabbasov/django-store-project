from django.contrib import admin


admin.site.site_header = "MultiShop administration"
admin.site.site_title = "MultiShop"


class ModelAdmin(admin.ModelAdmin):
    """Future app-wide admin customizations"""
