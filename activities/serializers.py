from django_filters import FilterSet
from rest_framework import serializers
from profiles.models import PatientProfile
from .models import Activity

class ActivitySerializer(serializers.ModelSerializer):
    patient = serializers.SlugRelatedField(read_only=True, slug_field='slug')
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = Activity
        fields = ('slug', 'patient', 'activitytype', 'shift', 'date')


class ActivityFilter(FilterSet):
    class Meta:
        model = Activity
        fields = ('activitytype', 'patient', 'shift')
