from django.urls import path
from .views import AppointmentListView, AppointmentCreateView, AppointmentDetailView, AppointmentUpdateView, AppointmentSoftDeleteView

urlpatterns = [
    path('', AppointmentListView.as_view(), name='list_appointment'),
    path('create/', AppointmentCreateView.as_view(), name='create_appointment'),
    path('<slug:slug>/', AppointmentDetailView.as_view(), name='detail_appointment'),
    path('update/<slug:slug>/', AppointmentUpdateView.as_view(), name='update_appointment'),
    path('delete/<slug:slug>/', AppointmentSoftDeleteView.as_view(), name='delete_appointment'),
]
