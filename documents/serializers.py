from django_filters import FilterSet
from rest_framework import serializers
from .models import DocumentType

class DocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentType
        fields = ('slug', 'name', 'description')


class DocumentTypeFilter(FilterSet):
    class Meta:
        model = DocumentType
        fields = ('name', )
