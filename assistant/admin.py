from django.contrib import admin
from .models import Assistant, Province, CityCountyTown
from django.utils.html import format_html


class AssistantAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'province', 'city_county_town', 'assistant_id']  # assistant_variable은 제거
    search_fields = ['name', 'assistant_id']
    list_filter = ['country', 'province', 'city_county_town']


admin.site.register(Assistant, AssistantAdmin)
admin.site.register(Province)
admin.site.register(CityCountyTown)