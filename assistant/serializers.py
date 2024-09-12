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

class AssistantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assistant
        fields = ['id', 'name', 'photo']