from django.contrib import admin
from .models import Assistant, Province, CityCountyTown
from django.utils.html import format_html


class AssistantAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'province', 'city_county_town', 'assistant_id', 'welcome_message']  # assistant_variable은 제거
    search_fields = ['name', 'assistant_id']
    list_filter = ['country', 'province', 'city_county_town']
    fields = (
        'assistant_id', 'name', 'photo', 'description', 'country', 'province', 'city_county_town',
        'document_id', 'question_1', 'question_2', 'question_3', 'question_4',
        'question_5', 'question_6', 'question_7', 'question_8', 'question_9', 'question_10', 'welcome_message'
    )


admin.site.register(Assistant, AssistantAdmin)
admin.site.register(Province)
admin.site.register(CityCountyTown)