from django.urls import path
from .views import HealthListView, HealthCreateView, HealthDetailView, HealthUpdateView, HealthSoftDeleteView, PatientListView, PatientCreateView, PatientDetailView, PatientUpdateView, PatientSoftDeleteView

urlpatterns = [
    path('', HealthListView.as_view(), name='list_health'),
    path('create/', HealthCreateView.as_view(), name='create_health'),
    path('patients/', PatientListView.as_view(), name='list_patient'),
    path('<slug:slug>/', HealthDetailView.as_view(), name='detail_health'),
    path('update/<slug:slug>/', HealthUpdateView.as_view(), name='update_health'),
    path('delete/<slug:slug>/', HealthSoftDeleteView.as_view(), name='delete_health'),
    path('patients/create/', PatientCreateView.as_view(), name='create_patient'),
    path('patients/<slug:slug>/', PatientDetailView.as_view(), name='detail_patient'),
    path('patients/update/<slug:slug>/', PatientUpdateView.as_view(), name='update_patient'),
    path('patients/delete/<slug:slug>/', PatientSoftDeleteView.as_view(), name='delete_patient')
]
