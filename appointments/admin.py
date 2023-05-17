from django.contrib import admin
from .models import Appointment

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'patient', 'health', 'previous', 'status')

admin.site.register(Appointment, AppointmentAdmin)
