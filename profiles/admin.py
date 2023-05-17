from django.contrib import admin
from .models import HealthProfile, PatientProfile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user', 'status')

admin.site.register(HealthProfile, ProfileAdmin)
admin.site.register(PatientProfile, ProfileAdmin)
