from django.contrib import admin
from .models import Client

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'user', 'created_at']
    list_filter = ['user', 'created_at']
    search_fields = ['name', 'phone', 'email']
