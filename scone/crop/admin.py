from django.contrib import admin

from scone.crop.models import Picture


@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    list_display = ('original_filename', 'image')
    list_filter = ('date_added', 'date_changed')
    search_fields = ('original_filename', 'uri')
    readonly_fields = ('original_filename', 'extension')
    date_hierarchy = 'date_added'
