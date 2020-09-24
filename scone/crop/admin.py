from django.contrib import admin

from scone.crop.models import Crop, Picture


@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    list_display = ('original_filename', 'image')
    list_filter = ('date_added', 'date_changed')
    search_fields = ('original_filename', 'uri')
    readonly_fields = ('original_filename', 'extension')
    date_hierarchy = 'date_added'


@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ('image',)
    list_filter = ('date_added', 'date_changed')
    search_fields = ('image__original_filename',)
    raw_id_fields = ('original_picture',)
    date_hierarchy = 'date_added'
