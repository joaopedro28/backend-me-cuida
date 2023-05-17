from django_filters import FilterSet
from rest_framework import serializers
from .models import HealthProfile, PatientProfile

class HealthProfileSerializer(serializers.ModelSerializer):
    documenttype = serializers.SlugRelatedField(read_only=True, slug_field='slug')

    class Meta:
        model = HealthProfile
        fields = ('slug', 'name', 'cpf', 'specialty', 'documentnumber', 'documenttype', 'admin')

class PatientProfileSerializer(serializers.ModelSerializer):
    health = serializers.SlugRelatedField(many=True, read_only=True, slug_field='slug')

    class Meta:
        model = PatientProfile
        fields = ('name', 'cpf', 'health')


class HealthProfileFilter(FilterSet):
    class Meta:
        model = HealthProfile
        fields = ('name', 'cpf', 'specialty', 'admin')

class PatientProfileFilter(FilterSet):
    class Meta:
        model = PatientProfile
        fields = ('name', 'cpf', 'health')
