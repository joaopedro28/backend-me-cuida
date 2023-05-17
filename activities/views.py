from django.http import Http404
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from profiles.models import PatientProfile
from .serializers import ActivitySerializer, ActivityFilter
from .models import Activity

class ActivityViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ActivitySerializer
    filter_class = ActivityFilter
    lookup_field = 'slug'

    def get_queryset(self):
        try:
            patient = PatientProfile.objects.get(user=self.request.user)
            return Activity.objects.filter(patient=patient, status=True).order_by('-date')
        except:
            return Activity.objects.none()

    def get_object(self):
        obj = super().get_object()
        try:
            patient = PatientProfile.objects.get(user=self.request.user)
        except:
            patient = None
        if not obj.status or patient!=obj.patient:
            raise Http404
        return obj

    def perform_create(self, serializer):
        serializer.save(patient=PatientProfile.objects.get(user=self.request.user))

    def perform_destroy(self, instance):
        instance.status = False
        instance.save()
