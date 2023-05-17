from django.http.response import HttpResponseRedirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.urls import reverse_lazy
from base_classes.mixins import SuperorAdminMixin
from base_classes.views import SoftDeleteView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from .serializers import DocumentTypeSerializer, DocumentTypeFilter
from .models import DocumentType
from .forms import DocumentTypeForm

class DocumentTypeListView(SuperorAdminMixin, ListView):
    queryset = DocumentType.objects.filter(status=True)
    template_name = 'documenttype_list.html'

class DocumentTypeCreateView(SuperorAdminMixin, CreateView):
    queryset = DocumentType.objects.filter(status=True)
    form_class = DocumentTypeForm
    template_name = 'documenttype_form.html'

class DocumentTypeDetailView(SuperorAdminMixin, DetailView):
    queryset = DocumentType.objects.filter(status=True)
    template_name = 'documenttype_detail.html'

class DocumentTypeUpdateView(SuperorAdminMixin, UpdateView):
    queryset = DocumentType.objects.filter(status=True)
    form_class = DocumentTypeForm
    template_name = 'documenttype_form.html'

class DocumentTypeSoftDeleteView(SuperorAdminMixin, SoftDeleteView):
    queryset = DocumentType.objects.filter(status=True)
    template_name = 'documenttype_softdelete.html'
    success_url = reverse_lazy('list_documenttype')

class DocumentTypeViewSet(ReadOnlyModelViewSet):
    queryset = DocumentType.objects.filter(status=True)
    permission_classes = [IsAuthenticated]
    serializer_class = DocumentTypeSerializer
    filter_class = DocumentTypeFilter
    lookup_field = 'slug'
