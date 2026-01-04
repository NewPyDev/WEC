from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'pieces_bought', 'pieces_sold', 'pieces_left', 'user']
    list_filter = ['user', 'created_at']
    search_fields = ['name', 'color']
    readonly_fields = ['pieces_left']
