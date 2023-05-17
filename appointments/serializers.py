from django_filters import FilterSet
from rest_framework import serializers
from .models import Appointment

class AppointmentSerializer(serializers.ModelSerializer):
    previous = serializers.SlugRelatedField(read_only=True, slug_field='slug')
    health = serializers.SlugRelatedField(read_only=True, slug_field='slug')
    patient = serializers.SlugRelatedField(read_only=True, slug_field='slug')

    class Meta:
        model = Appointment
        fields = ('slug', 'date', 'previous', 'health', 'patient', 'mean', 'quantitative0', 'quantitative1', 'quantitative2', 'quantitative3', 'quantitative4', 'note')


class AppointmentFilter(FilterSet):
    class Meta:
        model = Appointment
        fields = ('health', 'patient')