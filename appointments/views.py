from django.shortcuts import redirect
from django.http.response import HttpResponseRedirect
from django.template.context import RequestContext
from django.urls.base import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from MeCuida.views import user_context
from base_classes.mixins import NotPatientMixin
from base_classes.views import SoftDeleteView
from activities.models import Activity
from profiles.models import HealthProfile, PatientProfile
from .serializers import AppointmentSerializer, AppointmentFilter
from .models import Appointment
from .forms import AppointmentForm

class AppointmentListView(NotPatientMixin, ListView):
    queryset = Appointment.objects.filter(status=True)
    template_name = 'appointment_list.html'

    def get(self, request):
        aux = user_context(request)
        if aux['priority'] <= 2 and not 'self' in request.path[-5:]:
            return redirect('list_selfappointment')
        elif aux['priority'] >= 4 and 'self' in request.path[-5:]:
            return redirect('list_appointment')
        return super().get(request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        aux = user_context(self.request)
        if aux['priority']>=3 and not 'self' in self.request.path[-5:]:
            return context
        context['object_list'] = self.queryset.filter(health=aux['profile'])
        return context

class AppointmentCreateView(NotPatientMixin, CreateView):
    queryset = Appointment.objects.filter(status=True)
    form_class = AppointmentForm
    template_name = 'appointment_form.html'

    def get_initial(self):
        aux = user_context(self.request)
        if aux['priority']<=3:
            initial = {'health': aux['profile'].id}
        return initial

class AppointmentDetailView(NotPatientMixin, DetailView):
    queryset = Appointment.objects.filter(status=True)
    template_name = 'appointment_detail.html'

    def get(self, request, slug):
        aux = user_context(request)
        if aux['priority']<=2 and not aux['profile'] in self.object.health.all():
            return redirect('list_selfappointment')
        return super().get(request, slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        activities = Activity.objects.filter(status=True, patient=self.object.patient, date__lt=self.object.date).order_by('-date')
        if self.object.previous:
            activities = activities.exclude(date__lt=self.object.previous.date)
        context['activities'] = activities
        return context

class AppointmentUpdateView(NotPatientMixin, UpdateView):
    queryset = Appointment.objects.filter(status=True)
    form_class = AppointmentForm
    template_name = 'appointment_form.html'

    def get(self, request, slug):
        aux = user_context(request)
        if aux['priority']<=2 and not aux['profile'] in self.object.health.all():
            return redirect('list_selfappointment')
        return super().get(request, slug)

class AppointmentSoftDeleteView(NotPatientMixin, SoftDeleteView):
    queryset = Appointment.objects.filter(status=True)
    template_name = 'appointment_softdelete.html'
    success_url = reverse_lazy('list_appointment')

    def get(self, request, slug):
        aux = user_context(request)
        if aux['priority']<=2 and not aux['profile'] in self.object.health.all():
            return redirect('list_selfappointment')
        return super().get(request, slug)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.status = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

class AppointmentViewSet(ReadOnlyModelViewSet):
    queryset = Appointment.objects.filter(status=True)
    permission_classes = [IsAuthenticated]
    serializer_class = AppointmentSerializer
    filter_class = AppointmentFilter
    lookup_field = 'slug'

    def get_queryset(self):
        try:
            patient = PatientProfile.objects.get(user=self.request.user)
            return Appointment.objects.filter(patient=patient, status=True)
        except:
            return Appointment.objects.none()

    def get_object(self):
        obj = super().get_object()
        try:
            patient = PatientProfile.objects.get(user=self.request.user)
        except:
            patient = None
        if not obj.status or patient!=obj.patient:
            raise Http404
        return obj
