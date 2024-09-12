from django.contrib import admin
from .models import Assistant, Province, CityCountyTown
from django.utils.html import format_html


class AssistantAdmin(admin.ModelAdmin):
    list_display = ('name', 'province', 'city_county_town', 'assistant_variable', 'image_preview')

    def image_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="100" />'.format(obj.photo.url))
        return "No Image"

    image_preview.short_description = 'Image Preview'


admin.site.register(Assistant, AssistantAdmin)
admin.site.register(Province)
admin.site.register(CityCountyTown)