from django.contrib import admin
from .models import Contact

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'last_name', 'telephone', 'owner', 'created_at')
    list_filter = ('created_at', 'owner')
    search_fields = ('name', 'last_name', 'telephone')
    readonly_fields = ('created_at', 'updated_at')
