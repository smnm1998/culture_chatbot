from rest_framework import serializers
from .models import Province, CityCountyTown, Assistant

class CityCountyTownSerializer(serializers.ModelSerializer):
    class Meta:
        model = CityCountyTown
        fields = ['id', 'name']

class ProvinceSerializer(serializers.ModelSerializer):
    cities = CityCountyTownSerializer(many=True, read_only=True)

    class Meta:
        model = Province
        fields = ['id', 'name', 'cities']

# 어시스턴트 직렬화
class AssistantSerializer(serializers.ModelSerializer):
    city_county_town = CityCountyTownSerializer()  # 시군읍 정보 포함
    province = ProvinceSerializer()  # 도 정보 포함

    class Meta:
        model = Assistant
        fields = ['id', 'name', 'photo', 'description', 'country', 'province', 'city_county_town', 'document_id']