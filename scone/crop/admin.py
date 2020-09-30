from django.contrib import admin

from scone.crop.models import Crop, Picture


@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    list_display = ('uri', 'request_count')
    list_filter = ('date_added', 'date_changed')
    search_fields = ('uri',)
    readonly_fields = ('request_count',)
    date_hierarchy = 'date_added'


@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ('id', 'original_picture', 'request_count')
    list_filter = ('date_added', 'date_changed')
    search_fields = ('original_picture__uri',)
    raw_id_fields = ('original_picture',)
    readonly_fields = ('request_count',)
    date_hierarchy = 'date_added'
