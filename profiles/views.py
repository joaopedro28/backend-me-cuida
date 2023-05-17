from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.urls import reverse_lazy
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from MeCuida.views import user_context
from base_classes.mixins import SuperorAdminMixin, NotPatientMixin
from base_classes.views import SoftDeleteView
from activities.models import Activity
from .serializers import HealthProfileSerializer, PatientProfileSerializer, HealthProfileFilter, PatientProfileFilter
from .models import HealthProfile, PatientProfile
from .forms import HealthCreateForm, HealthUpdateForm, PatientCreateForm, PatientUpdateForm


# Profissionais de Saúde
class HealthListView(SuperorAdminMixin, ListView):
    queryset = HealthProfile.objects.filter(status=True)
    template_name = 'health_list.html'

class HealthCreateView(SuperorAdminMixin, CreateView):
    queryset = HealthProfile.objects.filter(status=True)
    form_class = HealthCreateForm
    template_name = 'health_form.html'

class HealthDetailView(SuperorAdminMixin, DetailView):
    queryset = HealthProfile.objects.filter(status=True)
    template_name = 'health_detail.html'

class HealthUpdateView(SuperorAdminMixin, UpdateView):
    queryset = HealthProfile.objects.filter(status=True)
    form_class = HealthUpdateForm
    template_name = 'health_form.html'

    def get_initial(self):
        initial = super().get_initial()
        health = self.get_object()
        user = health.user
        initial['username'] = user.username
        initial['email'] = user.email
        return initial

class HealthSoftDeleteView(SuperorAdminMixin, SoftDeleteView):
    queryset = HealthProfile.objects.filter(status=True)
    template_name = 'health_softdelete.html'
    success_url = reverse_lazy('list_health')

class HealthProfileViewSet(ReadOnlyModelViewSet):
    queryset = HealthProfile.objects.filter(status=True)
    permission_classes = [IsAuthenticated]
    serializer_class = HealthProfileSerializer
    filter_class = HealthProfileFilter
    lookup_field = 'slug'

    def get_queryset(self):
        try:
            patient = PatientProfile.objects.get(user=self.request.user)
            return HealthProfile.objects.filter(patientprofile=patient, status=True)
        except:
            return HealthProfile.objects.none()

    def get_object(self):
        obj = super().get_object()
        try:
            patient = PatientProfile.objects.get(user=self.request.user)
        except:
            patient = None
        if not obj.status or not obj in patient.health.all():
            raise Http404
        return obj

# Pacientes
class PatientListView(NotPatientMixin, ListView):
    queryset = PatientProfile.objects.filter(status=True)
    template_name = 'patient_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        aux = user_context(self.request)
        if aux['priority']>=3:
            return context
        context['object_list'] = self.queryset.filter(health=aux['profile'])
        return context

class PatientCreateView(NotPatientMixin, CreateView):
    queryset = PatientProfile.objects.filter(status=True)
    form_class = PatientCreateForm
    template_name = 'patient_form.html'

class PatientDetailView(NotPatientMixin, DetailView):
    queryset = PatientProfile.objects.filter(status=True)
    template_name = 'patient_detail.html'

    def dispatch(self, request, *args, **kwargs):
        temp = super().dispatch(request, *args, **kwargs)
        context = self.get_context_data()
        aux = user_context(self.request)
        if aux['priority']<=2 and not aux['profile'] in context['object'].health.all():
            return self.handle_no_permission()
        return temp

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activities'] = Activity.objects.filter(status=True, patient=self.object).order_by('-date')
        return context

class PatientUpdateView(NotPatientMixin, UpdateView):
    queryset = PatientProfile.objects.filter(status=True)
    form_class = PatientUpdateForm
    template_name = 'patient_form.html'

    def dispatch(self, request, *args, **kwargs):
        temp = super().dispatch(request, *args, **kwargs)
        context = self.get_context_data()
        aux = user_context(self.request)
        if aux['priority']<=2 and not aux['profile'] in context['object'].health.all():
            return self.handle_no_permission()
        return temp

    def get_initial(self):
        initial = super().get_initial()
        patient = self.get_object()
        user = patient.user
        initial['username'] = user.username
        initial['email'] = user.email
        return initial

class PatientSoftDeleteView(NotPatientMixin, SoftDeleteView):
    queryset = PatientProfile.objects.filter(status=True)
    template_name = 'patient_softdelete.html'
    success_url = reverse_lazy('list_patient')

    def dispatch(self, request, *args, **kwargs):
        temp = super().dispatch(request, *args, **kwargs)
        context = self.get_context_data()
        aux = user_context(self.request)
        if aux['priority']<=2 and not aux['profile'] in context['object'].health.all():
            return self.handle_no_permission()
        return temp

class PatientProfileViewSet(RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = PatientProfile.objects.filter(status=True)
    permission_classes = [IsAuthenticated]
    serializer_class = PatientProfileSerializer
    filter_class = PatientProfileFilter

    def list(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def get_object(self):
        try:
            patient = PatientProfile.objects.get(user=self.request.user)
        except:
            patient = None
        if not patient:
            raise Http404
        return patient
