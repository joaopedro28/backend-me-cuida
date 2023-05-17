from django.urls import path
from .views import DocumentTypeListView, DocumentTypeCreateView, DocumentTypeDetailView, DocumentTypeUpdateView, DocumentTypeSoftDeleteView

urlpatterns = [
    path('', DocumentTypeListView.as_view(), name='list_documenttype'),
    path('create/', DocumentTypeCreateView.as_view(), name='create_documenttype'),
    path('<slug:slug>/', DocumentTypeDetailView.as_view(), name='detail_documenttype'),
    path('update/<slug:slug>/', DocumentTypeUpdateView.as_view(), name='update_documenttype'),
    path('delete/<slug:slug>/', DocumentTypeSoftDeleteView.as_view(), name='delete_documenttype'),
]
