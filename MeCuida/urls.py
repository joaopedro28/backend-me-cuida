"""MeCuida URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from activities.views import ActivityViewSet
from appointments.views import AppointmentViewSet
from documents.views import DocumentTypeViewSet
from profiles.views import HealthProfileViewSet, PatientProfileViewSet
from .views import HomeView, LoginView, logout_view, SelfDetailView, SelfUpdateView, PasswordChangeView

router = routers.DefaultRouter()
router.register('activities', ActivityViewSet, basename='activity')
router.register('appointments', AppointmentViewSet, basename='appointment')
router.register('document_types', DocumentTypeViewSet, basename='document_type')
router.register('health_profiles', HealthProfileViewSet, basename='health_profile')
router.register('patient_profiles', PatientProfileViewSet, basename='patient_profile')

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('detail/', SelfDetailView.as_view(), name='detail'),
    path('update/', SelfUpdateView.as_view(), name='update'),
    path('password_change/', PasswordChangeView.as_view(), name='password_change'),
    path('profiles/', include('profiles.urls')),
    path('documents/', include('documents.urls')),
    path('appointments/', include('appointments.urls')),
    path('api_token/', obtain_auth_token),
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
]
